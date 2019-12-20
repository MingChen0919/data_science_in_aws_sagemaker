# H2O with Sagemaker

## Prepare a Docker image in AWS ECR
### Build an H2O Docker image

H2O has created such a Dockerfile which we can use directly. Download the Dockerfile and build the image directly from it.

```
wget https://raw.githubusercontent.com/h2oai/h2o3-sagemaker/master/automl/Dockerfile
docker build -t h2o:base .
```

**Issue:**
I was unable to build a Docker image with this Dockerfile. The error message I got is:

```
E: Package 'oracle-java8-installer' has no installation candidate
The command '/bin/sh -c echo 'DPkg::Post-Invoke {"/bin/rm -f /var/cache/apt/archives/*.deb || true";};' | tee /etc/apt/apt.conf.d/no-cache &&   echo "deb http://mirror.math.princeton.edu/pub/ubuntu xenial main universe" >> /etc/apt/sources.list &&   apt-get update -q -y &&   apt-get dist-upgrade -y &&   apt-get clean &&   rm -rf /var/cache/apt/* &&   DEBIAN_FRONTEND=noninteractive apt-get install -y wget unzip python-pip python-sklearn python-pandas python-numpy python-matplotlib software-properties-common python-software-properties &&   add-apt-repository -y ppa:webupd8team/java &&   apt-get update -q &&   echo debconf shared/accepted-oracle-license-v1-1 select true | debconf-set-selections &&   echo debconf shared/accepted-oracle-license-v1-1 seen true | debconf-set-selections &&   DEBIAN_FRONTEND=noninteractive apt-get install -y oracle-java8-installer &&   apt-get clean' returned a non-zero code: 100
```


### Push image to ECR
