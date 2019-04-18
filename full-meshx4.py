#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from subprocess import call
from mininet.topo import Topo



def myNetwork():

    net = Mininet( topo=None,
                   build=False,
                   ipBase='0.0.0.0/0')

    info( '*** Adding controller\n' )
    c0=net.addController(name='c0',
                      controller=Controller,
                      protocol='tcp',
                      port=6633)

    info( '*** Add switches\n')
    s6 = net.addSwitch('s6')
    s5 = net.addSwitch('s5')
    r1 = net.addHost('r1', cls=Node, ip='0.0.0.0')
    r1.cmd('sysctl -w net.ipv4.ip_forward=1')
    r2 = net.addHost('r2', cls=Node, ip='0.0.0.0')
    r2.cmd('sysctl -w net.ipv4.ip_forward=1')

    r3 = net.addHost('r3', cls=Node, ip='0.0.0.0')
    r3.cmd('sysctl -w net.ipv4.ip_forward=1')
    r4 = net.addHost('r4', cls=Node, ip='0.0.0.0')
    r4.cmd('sysctl -w net.ipv4.ip_forward=1')
    s8 = net.addSwitch('s8', cls=OVSKernelSwitch)
    s7 = net.addSwitch('s7', cls=OVSKernelSwitch)

    info( '*** Add hosts\n')
    h1 = net.addHost('h1', cls=Host, ip='12.12.12.1', defaultRoute='via 12.12.12.254')
    h4 = net.addHost('h4', cls=Host, ip='13.13.13.2', defaultRoute='via 13.13.13.254')
    h8 = net.addHost('h8', cls=Host, ip='10.10.10.1', defaultRoute='via 10.10.10.254')
    h3 = net.addHost('h3', cls=Host, ip='13.13.13.1', defaultRoute='via 13.13.13.254')
    h5 = net.addHost('h5', cls=Host, ip='11.11.11.2', defaultRoute='via 11.11.11.254')
    h2 = net.addHost('h2', cls=Host, ip='12.12.12.2', defaultRoute='via 12.12.12.254')
    h7 = net.addHost('h7', cls=Host, ip='10.10.10.2', defaultRoute='via 10.10.10.254')
    h6 = net.addHost('h6', cls=Host, ip='11.11.11.1', defaultRoute='via 11.11.11.254')


    info( '*** Add links\n')
    net.addLink(r1, r2, intfName1='r1-eth3', intfName2='r2-eth1')
    net.addLink(r1, r3, intfName1='r1-eth2', intfName2='r3-eth2')
    net.addLink(r1, r4, intfName1='r1-eth1', intfName2='r4-eth2')
    net.addLink(r4, r2, intfName1='r4-eth1', intfName2='r2-eth2')
    net.addLink(r2, r3, intfName1='r2-eth3', intfName2='r3-eth1')
    net.addLink(r3, r4, intfName1='r3-eth3', intfName2='r4-eth3')
    net.addLink(s8, r4, intfName2='r4-eth0')
    net.addLink(s7, r3, intfName2='r3-eth0')
    net.addLink(s7, h5)
    net.addLink(s7, h6)
    net.addLink(s8, h8)
    net.addLink(s8, h7)
    net.addLink(s5, r1, intfName2='r1-eth0')
    net.addLink(s6, r2, intfName2='r2-eth0')
    net.addLink(s5, h1)
    net.addLink(s5, h2)
    net.addLink(s6, h3)
    net.addLink(s6, h4)

    info( '*** Starting network\n')
    net.build()
    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info( '*** Starting switches\n')
    net.start()


    info('****** Configuire Routers\n')
    r1.cmdPrint('ifconfig r1-eth0 12.12.12.254 netmask 255.255.255.0')
    r1.cmdPrint('ifconfig r1-eth1 1.1.1.1 netmask 255.255.255.0')
    r1.cmdPrint('ifconfig r1-eth2 2.2.2.1 netmask 255.255.255.0')
    r1.cmdPrint('ifconfig r1-eth3 4.4.4.1 netmask 255.255.255.0')

    r2.cmdPrint('ifconfig r2-eth0 13.13.13.254 netmask 255.255.255.0')
    r2.cmdPrint('ifconfig r2-eth1 4.4.4.2 netmask 255.255.255.0')
    r2.cmdPrint('ifconfig r2-eth2 3.3.3.1 netmask 255.255.255.0')
    r2.cmdPrint('ifconfig r2-eth3 6.6.6.1 netmask 255.255.255.0')

    r3.cmdPrint('ifconfig r3-eth0 11.11.11.254 netmask 255.255.255.0')
    r3.cmdPrint('ifconfig r3-eth1 6.6.6.2 netmask 255.255.255.0')
    r3.cmdPrint('ifconfig r3-eth2 2.2.2.2 netmask 255.255.255.0')
    r3.cmdPrint('ifconfig r3-eth3 5.5.5.2 netmask 255.255.255.0')

    r4.cmdPrint('ifconfig r4-eth0 10.10.10.254 netmask 255.255.255.0')
    r4.cmdPrint('ifconfig r4-eth1 3.3.3.2 netmask 255.255.255.0')
    r4.cmdPrint('ifconfig r4-eth2 1.1.1.2 netmask 255.255.255.0')
    r4.cmdPrint('ifconfig r4-eth3 5.5.5.1 netmask 255.255.255.0')

    info('****** Configuire Routings\n')
    r1.cmdPrint('route add -net 10.10.10.0/24 gw 1.1.1.2')
    r1.cmdPrint('route add -net 11.11.11.0/24 gw 2.2.2.2')
    r1.cmdPrint('route add -net 13.13.13.0/24 gw 4.4.4.2')
    r1.cmdPrint('route add -net 3.3.3.0/24 gw 4.4.4.2')
    r1.cmdPrint('route add -net 5.5.5.0/24 gw 1.1.1.2')
    r1.cmdPrint('route add -net 6.6.6.0/24 gw 4.4.4.2 ')

    r2.cmdPrint('route add -net 10.10.10.0/24 gw 3.3.3.2')
    r2.cmdPrint('route add -net 11.11.11.0/24 gw 6.6.6.2')
    r2.cmdPrint('route add -net 12.12.12.0/24 gw 4.4.4.1')
    r2.cmdPrint('route add -net 2.2.2.0/24 gw 4.4.4.1')
    r2.cmdPrint('route add -net 5.5.5.0/24 gw 3.3.3.2')
    r2.cmdPrint('route add -net 1.1.1.0/24 gw 4.4.4.1')

    r3.cmdPrint('route add -net 10.10.10.0/24 gw 5.5.5.1')
    r3.cmdPrint('route add -net 12.12.12.0/24 gw 2.2.2.1')
    r3.cmdPrint('route add -net 13.13.13.0/24 gw 6.6.6.1')
    r3.cmdPrint('route add -net 1.1.1.0/24 gw 5.5.5.1')
    r3.cmdPrint('route add -net 4.4.4.0/24 gw 2.2.2.1')
    r3.cmdPrint('route add -net 3.3.3.0/24 gw 5.5.5.1')

    r4.cmdPrint('route add -net 12.12.12.0/24 gw 1.1.1.1')
    r4.cmdPrint('route add -net 11.11.11.0/24 gw 5.5.5.2')
    r4.cmdPrint('route add -net 13.13.13.0/24 gw 3.3.3.1')
    r4.cmdPrint('route add -net 4.4.4.0/24 gw 1.1.1.1')
    r4.cmdPrint('route add -net 2.2.2.0/24 gw 1.1.1.1')
    r4.cmdPrint('route add -net 6.6.6.0/24 gw 3.3.3.1')



    info( '*** Post configure switches and hosts\n')
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()

