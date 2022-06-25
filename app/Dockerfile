# FROM renanalves/containernet
FROM renanalves/containernet-androidtestbed
# LABEL maintainer="renan.alves@alu.ufc.br"

# COPY requiriments.txt /containernet/requiriments.txt
# RUN pip3 install -r /containernet/requiriments.txt

# RUN apt-get update && \
#   apt-get install -y adb && \
#   apt-get clean && \
#   rm -rf /var/lib/apt/lists/*

# COPY entrypoint.sh util/docker/entrypoint.sh

COPY app.py /containernet/app.py
COPY api /containernet/api
COPY testbed /containernet/testbed
COPY resources /containernet/resources
COPY android_controller /containernet/android_controller

# RUN mkdir /containernet/apks

EXPOSE 5000

ENTRYPOINT ["util/docker/entrypoint.sh"]
CMD ["python3", "/containernet/app.py"]
