import setproctitle
setproctitle.setproctitle('raftserver3')
import server
server.run_server(2)