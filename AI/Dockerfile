FROM ubuntu:18.04

RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get -y install wget gnupg gnupg2 gnupg1
RUN apt-get -y install software-properties-common

ADD . .

RUN wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/cuda-ubuntu1804.pin
RUN mv cuda-ubuntu1804.pin /etc/apt/preferences.d/cuda-repository-pin-600
RUN apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/7fa2af80.pub
CMD ls
RUN add-apt-repository "deb https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/ /"
RUN apt-get -y update

RUN wget http://developer.download.nvidia.com/compute/machine-learning/repos/ubuntu1804/x86_64/nvidia-machine-learning-repo-ubuntu1804_1.0.0-1_amd64.deb
RUN apt install -y ./nvidia-machine-learning-repo-ubuntu1804_1.0.0-1_amd64.deb
RUN apt-get -y update

RUN wget https://developer.download.nvidia.com/compute/machine-learning/repos/ubuntu1804/x86_64/libnvinfer7_7.1.3-1+cuda11.0_amd64.deb
RUN apt install -y ./libnvinfer7_7.1.3-1+cuda11.0_amd64.deb
RUN apt-get update

RUN apt-get -y --allow-downgrades install cuda-11-0
RUN apt-get -y --allow-downgrades install libcudnn8=8.0.4.30-1+cuda11.0
RUN apt-get -y --allow-downgrades install libcudnn8-dev=8.0.4.30-1+cuda11.0
RUN reboot

RUN apt-get -y --allow-downgrades install libnvinfer7=7.1.3-1+cuda11.0
RUN apt-get -y --allow-downgrades install libnvinfer-dev=7.1.3-1+cuda11.0
RUN apt-get -y --allow-downgrades install libnvinfer-plugin7=7.1.3-1+cuda11.0

RUN apt-get -y install python3 python3-pip

CMD pip --no-input install tensorflow-gpu pytroch numpy ecdsa