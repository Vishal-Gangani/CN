from mininet.topo import Topo
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.util import dumpNodeConnections

class TwoHostOneServerTopo(Topo):
    def build(self):
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        server = self.addHost('server')

        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')

        self.addLink(s1, s2)
        self.addLink(s2, s3)

        self.addLink(h1, s1)
        self.addLink(h2, s2)
        self.addLink(server, s3)

def run_custom_topology():
    net = Mininet(topo=TwoHostOneServerTopo())
    net.start()

    dumpNodeConnections(net.hosts)

    CLI(net)

    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    run_custom_topology()
