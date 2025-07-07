import setproctitle
setproctitle.setproctitle('raftserver1')
import server
server.run_server(0)