from os import system
from sys import argv

import nginx


IPs = argv[1].split()

# Lista com o servircos do MpOS e as portas
# Em caso de deploy de um novo app, adicione o Nome e a porta aqui
services = {
    'PingTcpServer': '40000',
    'PingUdpServer': '40001',
    'JitterUdpServer': '40005',
    'DeployAppTcpServer': '40020',
    'BandwidthTcpServer': '40010',
    'PersistenceTcpServer': '40011',
    'JitterRetrieveTcpServer': '40006',
    'RpcTcpServer_benchImage2': '36114',
    'DiscoveryServiceTcpServer': '30015',
    'DiscoveryMulticastService': '31000',
    'RpcTcpServer_matrixOperations': '36415',
    'RpcTcpServer_kotlin_matrixOperations': '36241',
    'RpcTcpServer_sourceafis': '36619'
}

conf = nginx.Conf()
stream = nginx.Stream()

for service_name, port in services.items():
    upstream = nginx.Upstream(service_name)
    for ip in IPs:
        upstream.add(
            nginx.Key(
                'server', '{}:{}'.format(ip, port) ) )

    server = nginx.Server()
    server.add(
        nginx.Key('listen', port),
        nginx.Key('proxy_pass', service_name) )

    stream.add(upstream, server)

conf.add(stream)

with open('/etc/nginx/nginx.conf', 'a') as file:
    nginx.dump(conf, file)

system('nginx -g "daemon off;"')