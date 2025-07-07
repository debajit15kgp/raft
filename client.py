import configparser
import grpc
import raft_pb2
import raft_pb2_grpc

CONFIG_FILE = "config.ini"

def get_stub():
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    base_address = config.get('Global', 'base_address')
    base_port = int(config.get('Servers', 'base_port'))
    active_servers = config.get('Servers', 'active').split(',')

    for server_id in active_servers:
        server_id = int(server_id)
        if server_id == -1:
            continue
        server_address = f'{base_address}:{str(base_port + server_id)}'
        channel = grpc.insecure_channel(server_address)
        stub = raft_pb2_grpc.KeyValueStoreStub(channel)
        try:
            _ = stub.ping(raft_pb2.Empty())
            return stub
        except Exception as e:
            pass
    print("No available servers!")

def get_state():
    # TODO: Ask what this is supposed to do
    stub = get_stub()
    try:
        response = stub.GetState(raft_pb2.Empty())
        print(f'Term = {response.term}')
    except Exception as e:
        print(e)

def set_val(key, value):
    stub = get_stub()
    request = raft_pb2.KeyValue(key=key, value=value)
    try:
        response = stub.Put(request)
        if response.success == False:
            print("Could not set value!")
    except Exception as e:
        print(e)

def get_val(key):
    stub = get_stub()
    request = raft_pb2.StringArg(arg=key)
    try:
        response = stub.Get(request)
        print(f'{response.key} = {response.value}')
    except Exception as e:
        print(e)

def run_client():
    print("Starting client...")
    while (1):
        try:
            user_input = input("Enter a command: ")
            user_input = user_input.split()
            instruction = user_input[0]
            
            if instruction == 'getstate' and len(user_input) == 1:
                get_state()
            elif instruction == 'put' and len(user_input) == 3 and user_input[1].isdigit():
                set_val(str(user_input[1]), user_input[2])
            elif instruction == 'get' and len(user_input) == 2 and user_input[1].isdigit():
                get_val(str(user_input[1]))
            elif instruction == 'quit' and len(user_input) == 1:
                print('Terminating client...')
                break
            else:
                print('Invalid command!')

        except KeyboardInterrupt:
            break
    return

if __name__ == "__main__":
    run_client()