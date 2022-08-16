import shlex as sh
import subprocess as sp

from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.net import Containernet
from mininet.link import TCLink
from mininet.node import Controller

from resources.utils import *


class ScenarioCreator:

  def __init__(self):
    setLogLevel('info')

    self.nodes = {}
    self.types = {}
    self.server_ips = ''

  def create_scenario(self, scenario_info):
    self.add_controller()
    
    """Creates a empty list if the field does not exist"""
    nodes = scenario_info.get( 'NODES', [] )
    switches = scenario_info.get( 'SWITCHES', [] )
    links = scenario_info.get( 'LINKS', [] )

    # TODO: reafactor this later
    # for now just try to read the list "REMOTE_SERVERS" from the JSON and add to the string
    for ip in scenario_info.get( 'REMOTE_SERVERS', [] ):
      self.server_ips += ' %s' % ip
    # # #

    for node in nodes:
      self.create_docker_node( node )

    for switch in switches:
      self.nodes[switch] = self.net.addSwitch( switch )

    for link in links:
      self.add_link( link )
    
    info(self.nodes)
  
  def add_controller(self):
    self.net = Containernet(controller=Controller)
    self.net.addController('c0')

  def create_docker_node(self, node):
    """
      Adds a docker container using 'mininet.net.addDocker'

      Args:
        node: dict with the name, ip, image and interface name
    """

    self.nodes[node.get('name')] = self.net.addDocker( 
      node.get('name'),
      ip=node.get('ip'),
      dimage=node.get('dimage') )
    connect_cntr_to_network( node.get('name') )
    
    self.nodes[node.get('interface')] = self.net.addSwitch( node.get('interface') )

    self.types[node.get('name')] = node.get('type')

    if node.get('type') == 'server':
      # adds the server ip to a list that will be used by the loadbalancer later
      self.server_ips += ' %s' % node.get("ip")

      # if set by the user, limits the amount of cpus the container can use
      if node.get('cpus') is not None:
        update_cntr_cpus( node.get('name'), node.get('cpus') )

    self.container_to_interface( node.get('name'), node.get('interface') )

  def container_to_interface(self, node, interface):
    """
      Creates a link between a docker node and a interface

      Args:
        node (str): key to the container obj in the self.nodes dict
        interface (str): key to the interface obj in the self.interfaces dict
    """

    self.net.addLink( self.nodes.get(node), self.nodes.get(interface ) )
  
  def add_link(self, link):
    """Key to the objects in the nodes dict"""
    f = link.get('from')
    t = link.get('to')

    self.net.addLink( self.nodes.get(f), self.nodes.get(t), cls=TCLink, delay=link.get('delay'), bw=link.get('bw'), jitter=link.get('jitter', None) )

  def run_scenario(self):
    for key, node in self.nodes.items():
      
      if self.types.get( key ) == "server":
        node.cmd( MPOS_START )
      elif self.types.get( key ) == "client":
        node.cmd( FORWARD_PORTS )
        node.cmd( ANDROID_EMU_START )
      elif self.types.get( key ) == "load-balance":
        node.cmd( "python3 /home/start.py '%s' &" % self.server_ips )
        self.server_ips = ''

    self.net.start()
    CLI(self.net)
  
  def stop_scenario(self):
    self.nodes = {}
    self.types = {}
    self.server_ips = ''
    
    self.net.stop()

    sp.call( sh.split('mn -c') )
