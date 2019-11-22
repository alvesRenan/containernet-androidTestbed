import docker

from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.net import Containernet
from mininet.link import TCLink
from mininet.node import Controller


class ScenarioCreator:

  def __init__(self):
    setLogLevel('info')

    self.net = Containernet(controller=Controller)
    self.net.addController('c0')

    self.nodes = {}
    self.types = {}

  def create_scenario(self, scenario_info):
    for node in scenario_info.get( 'NODES' ):
      self.create_docker_node( node )

    for switch in scenario_info.get( 'SWITCHES' ):
      self.create_switch( switch )

    for link in scenario_info.get( 'LINKS' ):
      self.add_link( link )

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

  def container_to_interface(self, c_name, i_name):
    """
      Creates a link between a docker node and a interface

      Args:
        c_name: key to the container obj in the self.nodes dict
        i_name: key to the interface obj in the self.interfaces dict
    """

    self.net.addLink( self.nodes.get(c_name), self.nodes.get(i_name) )

  def create_switch(self, switch_name):
    self.nodes[switch_name] = self.net.addSwitch( switch_name )
  
  def add_link(self, link):
    """Key to the objects in the nodes dict"""
    f = link.get('from')
    t = link.get('to')

    self.net.addLink( self.nodes.get(f), self.nodes.get(t), cls=TCLink, delay=link.get('delay'), bw=link.get('bw') )

  def run_scenario(self):
    for key, node in self.nodes.items():
      
      if self.types.get( key ) == "server":
        node.cmd("sh -c '/home/exec.sh' & ")
      else:
        node.cmd("sh -c '/root/port_forward.sh' & ")
        node.cmd("sh -c 'emulator @testAVD -memory 512 -partition-size 512 -no-boot-anim -accel auto -no-window -camera-back none -camera-front none -nojni -no-cache -no-audio' & ")

    self.net.start()
    CLI(self.net)
  
  def stop_scenario(self):
    self.net.stop()
