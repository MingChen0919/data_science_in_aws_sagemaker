#===========================================================================================
# Modified version of https://github.com/h2oai/h2o3-sagemaker/blob/master/automl/Dockerfile
#===========================================================================================


# Build an image that can do training and inference in SageMaker using
# H2o's automatic machine learning (AutoML)
# http://h2o-release.s3.amazonaws.com/h2o/rel-wheeler/2/docs-website/h2o-docs/automl.html
#
# Dockerfile template adapted from
# https://github.com/awslabs/amazon-sagemaker-examples/blob/master/advanced_functionality/scikit_bring_your_own/container/Dockerfile

FROM ubuntu:18.04

RUN apt-get -y update && apt-get -y upgrade && \
    apt-get -y --no-install-recommends install \
        wget \
        curl \
        unzip \
        apt-utils \
        software-properties-common \
        net-tools \
        nginx \
        ca-certificates \
        build-essential

RUN \
  echo 'DPkg::Post-Invoke {"/bin/rm -f /var/cache/apt/archives/*.deb || true";};' | tee /etc/apt/apt.conf.d/no-cache && \
  echo "deb http://mirror.math.princeton.edu/pub/ubuntu xenial main universe" >> /etc/apt/sources.list && \
  apt-get update -q -y && \
  apt-get dist-upgrade -y && \
  apt-get clean && \
  rm -rf /var/cache/apt/* && \
  DEBIAN_FRONTEND=noninteractive apt-get install -y wget unzip python-pip python-sklearn python-pandas python-numpy python-matplotlib software-properties-common python-software-properties && \
  echo debconf shared/accepted-oracle-license-v1-1 select true | debconf-set-selections && \
  echo debconf shared/accepted-oracle-license-v1-1 seen true | debconf-set-selections && \
  DEBIAN_FRONTEND=noninteractive apt-get install -y openjdk-8-jdk && \
  apt-get clean

RUN apt-get -y install \
      python3-setuptools \
      python3-pip \
      gdebi \
      python3-pandas \
      python3-numpy \
      python3-matplotlib \
      libxml2-dev \
      libssl-dev \
      libcurl4-openssl-dev \
      libgtk2.0-0 \
      iputils-ping

RUN wget http://h2o-release.s3.amazonaws.com/h2o/latest_stable -O latest && \
    wget --no-check-certificate -i latest -O /opt/h2o-latest.zip && \
    unzip -d /opt /opt/h2o-latest.zip && \
    rm /opt/h2o-latest.zip && \
    cd /opt && \
    mkdir program && \
    cd `find . -name 'h2o.jar' | sed 's/.\///;s/\/h2o.jar//g'` && \
    cp h2o.jar /opt/program && \
    touch /opt/program/flatfile.txt

RUN /usr/bin/pip3 install --upgrade --force-reinstall pip==9.0.3 && \
    /usr/bin/pip3 install numpy scipy scikit-learn pandas flask gevent gunicorn requests tabulate colorama future && \
    /usr/bin/pip3 install -f http://h2o-release.s3.amazonaws.com/h2o/latest_stable_Py.html h2o --user

# Set some environment variables. PYTHONUNBUFFERED keeps Python from buffering our standard
# output stream, which means that logs can be delivered to the user quickly. PYTHONDONTWRITEBYTECODE
# keeps Python from writing the .pyc files which are unnecessary in this case. We also update
# PATH so that the train and serve programs are found when the container is invoked.

ENV PYTHONUNBUFFERED=TRUE
ENV PYTHONDONTWRITEBYTECODE=TRUE

RUN pip install sagemaker-containers
ENTRYPOINT ["python3"]

