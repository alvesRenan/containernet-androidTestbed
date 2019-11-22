FROM androidsdk/android-22

COPY sources.list /etc/apt/sources.list

RUN apt-get update && \
  apt-get install -y \
  socat \
  net-tools \
  iproute2 \
  qemu-kvm \
  bridge-utils \
  cpu-checker \
  --no-install-recommends && \
  rm -rf /var/lib/apt/lists/*

COPY port_forward.sh /root

RUN chmod +x /root/port_forward.sh

EXPOSE 5554/tcp

EXPOSE 5555/tcp

EXPOSE 5902/tcp

RUN echo "no" | avdmanager create avd --force --name testAVD --abi google_apis/x86_64 --package 'system-images;android-22;google_apis;x86_64'

CMD /root/port_forward.sh 
