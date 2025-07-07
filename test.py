import configparser
import grpc, raft_pb2, raft_pb2_grpc

CONFIG_FILE = "config.ini"

def connect():
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    base_address = config.get('Global', 'base_address')
    base_port = config.get('Servers', 'base_port')
    active_servers = config.get('Servers', 'active').split(',')

    for server_id in active_servers:
        server_address = f'{base_address}:{base_port + server_id}'
        print(server_address)

config = configparser.ConfigParser()
config.read(CONFIG_FILE)
# connect(

channel = grpc.insecure_channel("127.0.0.1:50000")
stub = raft_pb2_grpc.ServerStub(channel)

request = raft_pb2.RequestVoteRequest(term=0, candidateId=1, lastLogIndex=0, lastLogTerm=0)
    
response = stub.requestVote(request)
print(response.term, response.voteGranted)