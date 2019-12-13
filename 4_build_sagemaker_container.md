**AWS has a lot of pre-built images for model training. Most of time, we would need to build our own sagemaker compatible images for data preprocessing.**

# 1. Put all Dockerfiles in `./aws/docker`

In our data_preprocessing Docker image, we install all necessary tool dependencies. An example Dockerfile can be like this:

```
FROM python:3.7-slim-buster

LABEL maintainer="ming.chen0919@gmail.com" version="0.1"

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    gcc \
    libgtk2.0-dev \
    python3-dev

RUN pip install sagemaker-containers \
    opencv-python \
    torch torchvision

ENTRYPOINT ["python3"]
```

**We SHOULD NOT copy our code to the Docker image. Otherwise we will need to rebuild the Docker image everytime we update our code.**

**sagemaker run a single command line tool to preprocess data or train model. if the command line tool (python script) depends on other custom python scripts. we can use sagemaker to copy these scripts from S3 to the container.** I will explain this in more details in the sagemaker preprocessing data section.


# 2. Create `.dockerignore` file

When Docker builds an image, it sends the current directory as building context. If the project folder has too much data, sending building context can take a very long time. The `.dockerignore` file is used to specify which folders to ignore. It works like `.gitignore`. An example `.dockerignore` file can be like this:

```
# ignore everything
*

# only keep folders that we need to copy to the image
!code
```

# 3. Build Docker image

We run the `docker build` command within the project root directory.

We tag the image with the format of **PROJFECT_NAME:FEATURE**. For example, if this image is for data preprocessing, then `FEATURE` could be `data_preprocessing`.

```
docker build -t PROJECT_NAME:FEATURE -f aws/docker/DOCKERFILE_NAME .
```



