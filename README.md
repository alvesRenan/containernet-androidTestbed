# containernet-androidTestbed

Integrating [androidTestBed](https://github.com/alvesRenan/androidTestBed) with [containernet](https://github.com/containernet/containernet).

## Build/Pull

```bash
# build the image
$ docker build -t renanalves/testbed-containernet .

# or pull the pre-build image 
$ docker pull renanalves/testbed-containernet
```

## Run

```bash
$ docker run --name testbed-containernet -it --rm --privileged --pid='host' -v /var/run/docker.sock:/var/run/docker.sock renanalves/testbed-containernet /bin/bash
```

## Examples
Run the testbed example:
```bash
python3 examples/android_testbed_example.py
```

Example scenario topology:

### c1 <---> s1 <---> s2 <---> serv1

where:
- c1: client container running Android emulator
- s1 and s2: containernet switches
- serv1: offloading server
- delay and bandwidth can be configured for each link connection

Checkout the [create_scenario_example.py](create_scenario_example.py) and [scenario_example.json](scenario_example.json) to see how to create other scenarios. 

## Running a test

Tests are executed outside of containernet. Before running, make sure the following dependencies are installed:

- ADB (Android Debbuging Bridge)
- Python version 3 and the [docker-py](https://github.com/docker/docker-py) library

To execute a test just run the [run_test_example.py](run_test_example.py)