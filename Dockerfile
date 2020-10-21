FROM containernet/containernet
LABEL maintainer="renan.alves@alu.ufc.br"

COPY entrypoint.sh util/docker/entrypoint.sh

COPY testbed/ /containernet/testbed
COPY README.md /containernet/testbed/README.md

COPY create_scenario_example.py /containernet/examples/android_testbed_example.py
COPY scenario_example.json /containernet/examples/scenario_example.json

ENTRYPOINT ["util/docker/entrypoint.sh"]
CMD ["python3", "examples/containernet_example.py"]