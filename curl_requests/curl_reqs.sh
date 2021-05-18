#!/bin/bash

case $1 in
  1|create)
    curl -X POST -H "Content-Type: application/json" http://localhost:5000/create -d @scenario_example.json
    ;;
  2|stop)
    curl -X GET http://localhost:5000/stop
    ;;
  3|send-apk)
    curl -X POST -F file=@'sample_app.apk' http://localhost:5000/send-apk/sample_app.apk
    ;;
  4|exec-test)
    curl -X POST -H "Content-Type: application/json" http://localhost:5000/exec -d @test_exec.json
    ;;
  5|all)
    curl -X GET http://localhost:5000/stop
    curl -X POST -H "Content-Type: application/json" http://localhost:5000/create -d @scenario_example.json
    curl -X POST -F file=@'../sample_app.apk' http://localhost:5000/send-apk/sample_app.apk
    sleep 15
    curl -X POST -H "Content-Type: application/json" http://localhost:5000/exec -d @test_exec.json
    ;;
  6|post-scenario)
    curl -X POST -H "Content-Type: application/json" http://localhost:5000/scenarios/test-scenario -d @scenario_example.json
    ;;
  7|get-scenario)
    curl -X GET http://localhost:5000/scenarios/test-scenario
    ;;
  *)
    echo "valid options: 'create (1)', 'stop (2)', 'send-apk (3)', 'exec-test (4)', 'all (5)', 'post-scenario (6)', 'get-scenario (7)'"
esac