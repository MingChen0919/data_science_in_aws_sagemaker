Sagemaker utilizes Docker containers to do all the jobs. AWS provides many pre-built Docker containers for us to use. Usually we can easily find an AWS pre-built Docker container with a common Machine Learning framework (sckit-learn, PyTorch, Tensorflow, MXNet, etc) installed. However, we will also need a Docker container to do data preprocessing. Such a Docker container usually does not exist. Therefore, we need to create our own. 

**We will create a single Docker container for both data preprocessing and model training. And we build such a Docker image on top of a selected AWS pre-built image.**


# 1. Find an AWS pre-built Sagemaker Container in GitHub

Go to https://github.com/aws and search for the GitHub repository of the sagemaker container that you are interested. For example, I can easily find the `sagemaker-pytorch-container` repository: https://github.com/aws/sagemaker-pytorch-container

Clone the GitHub repo to `./dockerfiles` folder:

```
cd dockerfiles && git clone https://github.com/aws/sagemaker-pytorch-container.git
```

# 2. Build sagemaker container

* Move into `./sagemaker-pytorch-container` folder: `cd ./sagemaker-pytorch-container`

* Build sagemaker base image:

```
docker build -t pytorch-base:1.1.0-gpu-py3 -f docker/1.1.0/base/Dockerfile.gpu --build-arg py_version=py3 .
```

* Build sagemaker final image:

```
pip3 install wheel
python setup.py bdist_wheel

docker build -t preprod-pytorch:1.1.0-gpu-py3 -f docker/1.1.0/final/Dockerfile.gpu --build-arg py_version=3 .
```

* Build custom image on top of sagemaker final image

Create file `custom-Dockerfile.gpu` and add the following content to file.

`Project_Folder/dockerfiles/custom-Dockerfile.gpu`

```
# Use the sagemaker final image as base image
FROM preprod-pytorch:1.1.0-gpu-py3

# Install project-specific dependencies
RUN pip3 install opencv-python

# Copy the ENTRYPOINT line from the final image Dockderfile
# Starts framework
ENTRYPOINT ["bash", "-m", "start_with_right_hostname.sh"]
```

In `Project_Folder/dockerfiles` run:

```
docker build -t custom-pytorch:1.1.0-gpu-py3 -f custom-Dockerfile.gpu .
```

