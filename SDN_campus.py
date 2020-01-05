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

def myNetwork():

    net = Mininet( topo=None,
                   build=False,
                   ipBase='10.0.0.0/8')

    info( '*** Adding controller\n' )
    c0=net.addController(name='c0',
                      controller=RemoteController,
                      port=6633)

    info( '*** Add switches\n')
    S_1_1 = net.addHost('S_1_1')
    S_1_2 = net.addHost('S_1_2')
    S_1_3 = net.addHost('S_1_3')
    S_2 = net.addHost('S_2')
    S_3_1 = net.addHost('S_3_1')
    S_3_2 = net.addHost('S_3_2')
    MLS1 = net.addHost('MLS1')
    MLS2 = net.addHost('MLS2')
    ISP = net.addHost('ISP')
    S_2_2 = net.addHost('S_2_2')
    S_3_3 = net.addHost('S_3_3')

    info( '*** Adding Routers\n')
    R1 = net.addHost('R1', cls=Node)
    R2 = net.addHost('R2', cls=Node)

    info( '*** Add hosts\n')
    info('*** Adding Level1 hosts\n')  # Summarization Address : 10.0.0.0/16
    info('*** 7 Offices\n')  # Subnet: 10.0.0.0/24  VLAN10
    for i in range(1, 9):   # Use a for loop to add hosts.
        net.addHost('L1_OH' + str(i), cls=Host, ip='10.0.0.' + str(i) + '/24', defaultRoute = 'via 10.0.0.254 dev L1_OH' + str(i) + '-eth0')
        net.addLink('L1_OH' + str(i), S_1_1, intfName2 = 'S_1_1-eth0' + str(i))

    info('*** 40 lab PCs\n')  # Subnet: 10.0.1.0/24  VLAN11
    for i in range(1,41):
        net.addHost('L1_LH' + str(i), cls=Host, ip='10.0.1.' + str(i) + '/24', defaultRoute = 'via 10.0.1.254 dev L1_LH' + str(i) + '-eth0')
        net.addLink('L1_LH' + str(i), S_1_2, intfName2 = 'S_1_2-eth0' + str(i))

    info( '*** 1 lab-Tut PCs\n')        # Subnet: 10.0.2.0/24   VLAN12
    net.addHost('L1_LT', cls=Host, ip='10.0.2.0/24', defaultRoute='via 10.0.2.254 dev L1_LT-eth0')
    net.addLink('L1_LT', S_1_3, intfName2='S_1_3-eth0')

    info( '*** 10 Servers\n')       # Subnet: 10.0.4.0/24     VLAN14
    for i in range(1,11):
        net.addHost('L1_SH' + str(i), cls=Host, ip='10.0.4.' + str(i) + '/24', defaultRoute = 'via 10.0.4.254 dev L1_SH' + str(i) + '-eth0')
        net.addLink('L1_SH' + str(i), S_1_3, intfName2 = 'S_1_3-eth1' + str(i))

    info( '*** Adding Level2 hosts\n')      # Summarization Address : 10.1.0.0/16
    info( '*** Sofeware House 10 PCs\n')  # Subnet: 10.1.0.0/24     VLAN20
    for i in range(1,11):
        net.addHost('L2_SH' + str(i), cls=Host, ip='10.1.0.' + str(i) + '/24', defaultRoute = 'via 10.1.0.254 dev L2_SH' + str(i) + '-eth0')
        net.addLink('L2_SH' + str(i), S_2, intfName2 = 'S_2-eth0' + str(i))

    info( '*** Adding Level3 hosts\n')      # Summarization Address : 10.2.0.0/16
    info('*** R&D Lab 30 PCs\n')  # Subnet: 10.2.0.0/24     VLAN30
    for i in range(1,31):
        net.addHost('L3_LH' + str(i), cls=Host, ip='10.2.0.' + str(i) + '/24', defaultRoute = 'via 10.2.0.254 dev L3_LH' + str(i) + '-eth0')
        net.addLink('L3_LH' + str(i), S_3_1, intfName2 = 'S_3_1-eth0' + str(i))

    info('*** Management 5 PCs\n')  # Subnet: 10.2.1.0/24   VLAN31
    for i in range(1,6):
        net.addHost('L3_MH' + str(i), cls=Host, ip='10.2.1.' + str(i) + '/24', defaultRoute = 'via 10.2.1.254 dev L3_MH' + str(i) + '-eth0')
        net.addLink('L3_MH' + str(i), S_3_2, intfName2 = 'S_3_2-eth0' + str(i))

    info('*** APs\n')  #subnet: 10.4.0.0/22    VLAN40
    net.addHost('L1AP', cls=Host,ip='10.4.0.1/22', defaultRoute = 'via 10.4.0.254 dev L1AP-eth0')
    net.addHost('L2AP', cls=Host,ip='10.4.0.2/22', defaultRoute = 'via 10.4.0.253 dev L2AP-eth0')
    net.addHost('L3AP', cls=Host,ip='10.4.0.3/22', defaultRoute = 'via 10.4.0.252 dev L3AP-eth0')
    net.addLink('L1AP', S_1_3, intfName2 = 'S_1_3-eth99')
    net.addLink('L2AP', S_2_2, intfName2 = 'S_2_2-eth99')
    net.addLink('L3AP', S_3_3, intfName2 = 'S_3_3-eth99')


    info('*** Network Links\n')

    net.addLink(S_1_1, MLS1, intfName1='S_1_1-eth81', intfName2='MLS1-eth10')  #VLAN10
    net.addLink(S_1_2, MLS1, intfName1='S_1_2-eth81', intfName2='MLS1-eth11')  #VLAN11
    net.addLink(S_1_3, MLS1, intfName1='S_1_3-eth81', intfName2='MLS1-eth12')  #VLAN12 VLAN14 VLAN40
    net.addLink(S_2, MLS1, intfName1='S_2-eth81', intfName2='MLS1-eth20')  #VLAN20
    net.addLink(S_2_2, MLS1, intfName1='S_2_2-eth81', intfName2='MLS1-eth24')  #VLAN40

    net.addLink(S_3_1, MLS1, intfName1='S_3_1-eth81',intfName2='MLS1-eth30') #VLAN30
    net.addLink(S_3_2, MLS1, intfName1='S_3_2-eth81',intfName2='MLS1-eth31') #VLAN31
    net.addLink(S_3_3, MLS1, intfName1='S_3_3-eth81',intfName2='MLS1-eth34') #VLAN40

    net.addLink(S_1_1, MLS2, intfName1='S_1_1-eth91', intfName2='MLS2-eth10')  #VLAN10
    net.addLink(S_1_2, MLS2, intfName1='S_1_2-eth91', intfName2='MLS2-eth11')  #VLAN11
    net.addLink(S_1_3, MLS2, intfName1='S_1_3-eth91', intfName2='MLS2-eth12')  #VLAN12 VLAN14 VLAN40
    net.addLink(S_2, MLS2, intfName1='S_2-eth91', intfName2='MLS2-eth20')  #VLAN20
    net.addLink(S_2_2, MLS2, intfName1='S_2_2-eth91', intfName2='MLS2-eth24')  #VLAN40

    net.addLink(S_3_1, MLS2, intfName1='S_3_1-eth91',intfName2='MLS2-eth30') #VLAN30
    net.addLink(S_3_2, MLS2, intfName1='S_3_2-eth91',intfName2='MLS2-eth31') #VLAN31 VLAN40
    net.addLink(S_3_3, MLS2, intfName1='S_3_3-eth91',intfName2='MLS2-eth34') #VLAN40

    net.addLink(R1, MLS1, intfName1='R1-eth3', intfName2='MLS1-eth100')
    net.addLink(R2, MLS2, intfName1='R2-eth3', intfName2='MLS2-eth100')
    net.addLink(R1, R2, intfName1='R1-eth1',intfName2='R2-eth1')
    net.addLink(ISP,R1 ,intfName1='ISP-eth1', intfName2='R1-eth0')
    net.addLink(ISP,R2 ,intfName1='ISP-eth2', intfName2='R2-eth0')

    info( '*** Starting network\n')
    net.build()
    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info( '*** Starting switches\n')
    net.start()

    info( '*** Post configure switches and hosts\n')
    #floor2 config
    S_2.cmd("vconfig add S_2-eth81 20")
    S_2_2.cmd("vconfig add S_2_2-eth81 40")

    S_2.cmd("brctl addbr brvlan20")
    S_2_2.cmd("brctl addbr brvlan40")

    S_2.cmd("brctl addif brvlan20 S_2-eth81")
    S_2_2.cmd("brctl addif brvlan40 S_2_2-eth81")
    S_2_2.cmd("brctl addif brvlan40 S_2_2-eth99")
    for i in range(1,11):
        S_2.cmd("brctl addif brvlan20 S_2-eth0" + str(i))

    S_2.cmd("ifconfig brvlan20 up")
    S_2_2.cmd("ifconfig brvlan40 up")

    #floor3 config
    S_3_1.cmd("vconfig add S_3_1-eth81 30")
    S_3_2.cmd("vconfig add S_3_2-eth81 31")
    S_3_3.cmd("vconfig add S_3_3-eth81 40")


    S_3_1.cmd("brctl addbr brvlan30")
    S_3_2.cmd("brctl addbr brvlan31")
    S_3_3.cmd("brctl addbr brvlan40")

    S_3_1.cmd("brctl addif brvlan30 S_3_1-eth81")
    S_3_2.cmd("brctl addif brvlan31 S_3_2-eth81")
    S_3_3.cmd("brctl addif brvlan40 S_3_3-eth81")
    S_3_3.cmd("brctl addif brvlan40 S_3_3-eth99")

    for i in range(1,31):
        S_3_1.cmd("brctl addif brvlan30 S_3_1-eth0" + str(i))
    for i in range(1,6):
        S_3_2.cmd("brctl addif brvlan31 S_3_2-eth0" + str(i))

    S_3_1.cmd("ifconfig brvlan30 up")
    S_3_2.cmd("ifconfig brvlan31 up")
    S_3_3.cmd("ifconfig brvlan40 up")

    # floor1 config
    S_1_1.cmd("vconfig add S_1_1-eth81 10")
    S_1_2.cmd("vconfig add S_1_2-eth81 11")
    S_1_1.cmd("brctl addbr brvlan10")
    S_1_2.cmd("brctl addbr brvlan11")
    S_1_3.cmd("brctl addbr brvlan12")
    S_1_3.cmd("brctl addbr brvlan14")
    S_1_3.cmd("brctl addbr brvlan40")
    S_1_1.cmd("brctl addif brvlan10 S_1_1-eth81")
    S_1_2.cmd("brctl addif brvlan11 S_1_2-eth81")
    S_1_3.cmd("vconfig add S_1_3-eth81 12")
    S_1_3.cmd("vconfig add S_1_3-eth81 14")
    S_1_3.cmd("vconfig add S_1_3-eth81 40")
    S_1_3.cmd("ifconfig S_1_3-eth81.12 up")
    S_1_3.cmd("ifconfig S_1_3-eth81.14 up")
    S_1_3.cmd("ifconfig S_1_3-eth81.40 up")
    S_1_3.cmd("brctl addif brvlan12 S_1_3-eth81.12")
    S_1_3.cmd("brctl addif brvlan14 S_1_3-eth81.14")
    S_1_3.cmd("brctl addif brvlan40 S_1_3-eth81.40")
    for i in range(1, 9):   # Use a for loop to add hosts.
        S_1_1.cmd("brctl addif brvlan10 S_1_1-eth0" + str(i))
    for i in range(1,41):
        S_1_2.cmd("brctl addif brvlan11 S_1_2-eth0" + str(i))
    S_1_3.cmd("brctl addif brvlan12 S_1_3-eth0")
    for i in range(1,11):
        S_1_3.cmd("brctl addif brvlan14 S_1_3-eth1" + str(i))
    S_1_3.cmd("brctl addif brvlan40 S_1_3-eth99")
    S_1_1.cmd("ifconfig brvlan10 up")
    S_1_2.cmd("ifconfig brvlan11 up")
    S_1_3.cmd("ifconfig brvlan12 up")
    S_1_3.cmd("ifconfig brvlan14 up")
    S_1_3.cmd("ifconfig brvlan40 up")

    # MLS1 supporting all the vlans
    MLS1.cmd("vconfig add MLS1-eth10 10")
    MLS1.cmd("vconfig add MLS1-eth11 11")
    MLS1.cmd("vconfig add MLS1-eth12 12")
    MLS1.cmd("vconfig add MLS1-eth12 14")
    MLS1.cmd("vconfig add MLS1-eth12 40")
    MLS1.cmd("vconfig add MLS1-eth20 20")
    MLS1.cmd("vconfig add MLS1-eth24 40")
    MLS1.cmd("vconfig add MLS1-eth30 30")
    MLS1.cmd("vconfig add MLS1-eth31 31")
    MLS1.cmd("vconfig add MLS1-eth34 40")

    # MLS1 configuring the interfaces
    MLS1.cmd("echo 1>/proc/sys/net/ipv4/ip_forward")
    MLS1.cmd("ifconfig MLS1-eth10 10.0.0.254/24")
    MLS1.cmd("ifconfig MLS1-eth11 10.0.1.254/24")
    MLS1.cmd("ifconfig MLS1-eth12.12 10.0.2.254/24")
    MLS1.cmd("ifconfig MLS1-eth12.14 10.0.4.254/24")
    MLS1.cmd("ifconfig MLS1-eth12.40 10.4.0.254/24")
    MLS1.cmd("ifconfig MLS1-eth20 10.1.0.254/24")
    MLS1.cmd("ifconfig MLS1-eth24 10.4.0.253/24")
    MLS1.cmd("ifconfig MLS1-eth30 10.2.0.254/24")
    MLS1.cmd("ifconfig MLS1-eth31 10.2.1.254/24")
    MLS1.cmd("ifconfig MLS1-eth34 10.4.0.252/24")


    MLS1.cmd("ifconfig MLS1-eth100 10.3.2.2/24")
    MLS2.cmd("ifconfig MLS2-eth100 10.3.4.2/24")

    # Routing on ISP, MLS1,2, R1,2
    ISP.cmd("ifconfig ISP-eth1 220.110.0.1/30")
    ISP.cmd("ifconfig ISP-eth2 220.110.0.5/30")
    R1.cmd("ifconfig R1-eth0 220.110.0.2/30")
    R2.cmd("ifconfig R2-eth0 220.110.0.6/30")
    R1.cmd("route add -net 0.0.0.0/0 gw 220.110.0.1")
    R2.cmd("route add -net 0.0.0.0/0 gw 220.110.0.5")
    R1.cmd("ifconfig R1-eth1 10.3.1.1/24")
    R2.cmd("ifconfig R2-eth1 10.3.1.2/24")
    R1.cmd("ifconfig R1-eth3 10.3.2.1/24")
    R2.cmd("ifconfig R2-eth3 10.3.4.1/24")
    MLS1.cmd("route add -net 0.0.0.0/0 gw 10.3.2.1")
    MLS2.cmd("route add -net 0.0.0.0/0 gw 10.3.4.1")
    R1.cmd("route add -net 10.0.0.0/8 gw 10.3.2.2")
    ISP.cmd("route add -net 10.0.0.0/8 gw 220.110.0.2")
    #ISP.cmd("route add -net 10.0.0.0/8 gw 220.110.0.6")





    info('*** Router interface config\n')



    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()

