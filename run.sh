#!/bin/bash

function default_init() {
	modprobe openvswitch && docker-compose up -d
}

function build() {
	docker build -t renanalves/containernet-androidtestbed .
}

function build_test() {
	docker rmi renanalves/containernet-androidtestbed:test
	docker build -t renanalves/containernet-androidtestbed:test .
}

function kill_compose() {
	docker-compose kill && docker-compose rm -f
}

case $1 in
	build)
		build
		;;
	build-test)
		build_test
		;;
	kill)
		kill_compose
		;;
	pipeline)
		kill_compose
		build_test
		default_init
		;;
	*)
		default_init
		;;
esac
