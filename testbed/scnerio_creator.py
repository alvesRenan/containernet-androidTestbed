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

  def create_scenario(self, scenario_info):
    self.add_controller()
    
    """Creates a empty list if the field does not exist"""
    nodes = scenario_info.get( 'NODES', [] )
    switches = scenario_info.get( 'SWITCHES', [] )
    links = scenario_info.get( 'LINKS', [] )

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
    
    self.nodes[node.get('interface')] = self.net.addSwitch( node.get('interface') )

    self.types[node.get('name')] = node.get('type')

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

    self.net.addLink( self.nodes.get(f), self.nodes.get(t), cls=TCLink, delay=link.get('delay'), bw=link.get('bw') )

  def run_scenario(self):
    for key, node in self.nodes.items():
      
      if self.types.get( key ) == "server":
        node.cmd( MPOS_START )
      else:
        node.cmd( FORWARD_PORTS )
        node.cmd( ANDROID_EMU_START )

    self.net.start()
    CLI(self.net)
  
  def stop_scenario(self):
    self.net.stop()

    sp.call( sh.split('mn -c') )
