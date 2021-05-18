# FROM renanalves/containernet-androidtestbed
FROM renanalves/containernet
LABEL maintainer="renan.alves@alu.ufc.br"

COPY requiriments.txt /containernet/requiriments.txt
RUN pip3 install -r /containernet/requiriments.txt

RUN apt-get update && \
  apt-get install -y adb && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/*

COPY entrypoint.sh util/docker/entrypoint.sh

# COPY README.md /containernet/testbed/README.md

COPY app.py /containernet/app.py
COPY api /containernet/api
COPY testbed /containernet/testbed
COPY resources /containernet/resources
COPY android_controller /containernet/android_controller

# COPY create_scenario_example.py /containernet/examples/android_testbed.py
# COPY scenario_example.json /containernet/examples/scenario_example.json

EXPOSE 5000

ENTRYPOINT ["util/docker/entrypoint.sh"]
CMD ["python3", "/containernet/app.py"]