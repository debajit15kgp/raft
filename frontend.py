import grpc, os, signal
import raft_pb2
import raft_pb2_grpc
from concurrent import futures
import configparser
import subprocess
import time
import sys
from typing import Dict, List, Optional, Tuple

CONFIG_FILE = "config.ini"
FRONTEND_PORT = 8001
BASE_SERVER_PORT = 9000

class FrontEndService(raft_pb2_grpc.FrontEndServicer):
    def __init__(self):
        self.address_map = {} 
        self.raft_processes = []
        self.duplicate_request_cache = {} 
        self.current_leader = None
        self.base_address = '127.0.0.1'
    
    def get_stub(self):
        config = configparser.ConfigParser()
        config.read(CONFIG_FILE)
        base_address = config.get('Global', 'base_address')
        base_port = int(config.get('Servers', 'base_port'))
        active_servers = config.get('Servers', 'active').split(',')

        for server_id in active_servers:
            server_id = int(server_id)
            if server_id == -1:
                continue
            server_address = f'{base_address}:{str(base_port + server_id + 1)}'
            channel = grpc.insecure_channel(server_address)
            stub = raft_pb2_grpc.KeyValueStoreStub(channel)
            try:
                _ = stub.ping(raft_pb2.Empty())
                return stub
            except Exception as e:
                pass
        print("No available servers!")

    def find_new_leader(self):
        for server_id, address in self.address_map.items():
            try:
                channel = grpc.insecure_channel(address)
                stub = raft_pb2_grpc.KeyValueStoreStub(channel)
                print(f"Trying server {server_id} at {address}")
                
                state = stub.GetState(raft_pb2.Empty())
                print(f"Server {server_id} state:", state)
                
                if state.isLeader:
                    print(f"Found new leader: Server {server_id}")
                    return (server_id, stub)
                    
            except Exception as e:
                print(f"Error with server {server_id}: {str(e)}")
                continue
        print("No leader found")
        return None

    def get_leader_stub(self, force_find: bool = False) -> Optional[raft_pb2_grpc.KeyValueStoreStub]:  # Changed return type
        if not force_find and self.current_leader:
            try:
                state = self.current_leader[1].getState(raft_pb2.Empty())
                if state.isLeader:
                    return self.current_leader[1]
            except:
                self.current_leader = None

        self.current_leader = self.find_new_leader()
        return self.current_leader[1] if self.current_leader else None

    def Put(self, request, context):
        cache_key = (request.ClientId, request.RequestId)
        if cache_key in self.duplicate_request_cache:
            return self.duplicate_request_cache[cache_key]

        for _ in range(3):
            leader_stub = self.get_stub()
            print(leader_stub, "00")
            if not leader_stub:
                return raft_pb2.Reply(wrongLeader=True, error="No leader available")

            try:
                server_request = raft_pb2.KeyValue(
                    key=str(request.key),
                    value=str(request.value)
                )
                print("Trying")
                response = leader_stub.Put(server_request)
                
                reply = raft_pb2.Reply(
                    wrongLeader=not response.success,
                    error="" if response.success else "Put failed"
                )
                
                if response.success:
                    self.duplicate_request_cache[cache_key] = reply
                return reply

            except Exception as e:
                self.current_leader = None
                continue

        return raft_pb2.Reply(wrongLeader=True, error="Operation failed after retries")

    def Get(self, request, context):
        for _ in range(3):
            leader_stub = self.get_stub()
            if not leader_stub:
                return raft_pb2.Reply(wrongLeader=True, error="No servers available")
            try:
                server_request = raft_pb2.StringArg(arg=str(request.key))
                response = leader_stub.Get(server_request)

                print(response)
                return raft_pb2.Reply(
                    wrongLeader=False,
                    value=response.value
                )

            except Exception as e:
                self.current_leader = None
                continue

        return raft_pb2.Reply(wrongLeader=True, error="Operation failed after retries")

    def Replace(self, request, context):
        return self.Put(request, context)

    def StartRaft(self, request, context):
        try:
            num_servers = request.arg
            if num_servers <= 0:
                return raft_pb2.Reply(wrongLeader=True, error="Number of servers must be positive")
            
            self.cleanup_raft_processes()
            self.current_leader = None
            self.address_map.clear()

            config = configparser.ConfigParser()
            config.read(CONFIG_FILE)
            config.set('Servers', 'active', ",".join(map(str, range(num_servers))))
            with open(CONFIG_FILE, "w+") as configfile:
                config.write(configfile)

            # Setup address map
            for i in range(num_servers):
                server_id = i  # Server IDs start from 1
                server_port = BASE_SERVER_PORT + server_id + 1
                self.address_map[server_id] = f"{self.base_address}:{server_port}"

            print(f"Starting RAFT cluster with {num_servers} servers")
            print(f"Address map: {self.address_map}")

            # Start each server in a new terminal
            current_dir = os.path.dirname(os.path.abspath(__file__))
            server_script = os.path.join(current_dir, "server.py")

            for server_id in range(0, num_servers):
                try:
                    # Command to open new terminal and run server for macOS

                    proc_script = f"""import setproctitle
setproctitle.setproctitle('raftserver{server_id+1}')
import server
server.run_server({server_id})"""
                    proc_script_path = os.path.join(current_dir, f"start_proc_{server_id}.py")
                    with open(proc_script_path, "w") as f:
                        f.write(proc_script)

                    # Command for Terminal to activate venv and run the script
                    cmd = ['osascript', '-e', f'''
                        tell application "Terminal"
                            do script "cd {current_dir} && pip install setproctitle && python3 {proc_script_path}"
                            activate
                        end tell
                    ''']
                    
                    process = subprocess.Popen(
                        cmd,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE
                    )
                    
                    self.raft_processes.append((process, None))
                    print(f"Started server {server_id} in new terminal window")
                    
                except Exception as e:
                    print(f"Error starting server {server_id}: {str(e)}")
                    self.cleanup_raft_processes()
                    return raft_pb2.Reply(wrongLeader=True, error=f"Failed to start server {server_id}")

            return raft_pb2.Reply(wrongLeader=False)
                
        except Exception as e:
            print(f"Error in StartRaft: {str(e)}")
            self.cleanup_raft_processes()
            return raft_pb2.Reply(wrongLeader=True, error=str(e))

    def cleanup_raft_processes(self):
        """Clean up running RAFT processes."""
        # On macOS, close terminal windows running the servers
        try:
            cmd = ['osascript', '-e', '''
                tell application "Terminal"
                    set windowCount to count windows
                    repeat with x from 1 to windowCount
                        set currentTab to selected tab of window x
                        if (processes of currentTab contains "python3") and (processes of currentTab contains "server.py") then
                            close window x
                        end if
                    end repeat
                end tell
            ''']
            subprocess.run(cmd)
        except Exception as e:
            print(f"Error cleaning up terminal windows: {str(e)}")

        # Clear process list
        self.raft_processes.clear()

        # Kill any remaining server processes
        try:
            subprocess.run(['pkill', '-f', 'server.py'], check=False)
        except:
            pass

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    frontend = FrontEndService()
    raft_pb2_grpc.add_FrontEndServicer_to_server(frontend, server)
    server.add_insecure_port(f'[::]:{FRONTEND_PORT}')
    
    try:
        server.start()
        print(f"Frontend server started on port {FRONTEND_PORT}")
        server.wait_for_termination()
    finally:
        frontend.cleanup_raft_processes()

if __name__ == '__main__':
    serve()