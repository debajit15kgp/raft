import setproctitle
setproctitle.setproctitle('raftserver2')
import server
server.run_server(1)