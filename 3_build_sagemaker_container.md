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

# 3. Publish Docker image to AWS ECR 

(Refeference: https://docs.aws.amazon.com/AmazonECR/latest/userguide/docker-basics.html)

## Create an ECR repository: 

* Refer to https://docs.aws.amazon.com/AmazonECR/latest/userguide/ECR_GetStarted.html

## Register the docker image in ECR

* **Before you start, make sure you have created an `IAM User` for ECR access and add the access key credentials to the `~/.aws/credentials` file in your local computer**. You will also need to install **aws cli**

* **Use **aws cli** to get login information for authenticate Docker to interact with your AWS ECR resource**

  + `aws2 ecr get-login --region us-east-2 --no-include-email` --profile ming_ecr
  + the above command will output something like this: `docker login -u AWS -p password https://aws_account_id.dkr.ecr.us-east-1.amazonaws.com`. You run the output as a command to login your Docker
  
* **Push docker image to ECR**
  
  + Tag the image with ECR RepositoryURI: `docker tag custom-pytorch:1.1.0-gpu-py3 aws_account_id.dkr.ecr.region.amazonaws.com/deep-learning`
  + Push tagged image: `docker push aws_account_id.dkr.ecr.region.amazonaws.com/deep-learning`






