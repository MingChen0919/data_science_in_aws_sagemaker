# H2O with Sagemaker

## Prepare a Docker image in AWS ECR
### Build an H2O Docker image

Build a Docker image using this [Dockerfile](Dockerfile)

```
docker build -t h2o:base .
```

### Push image to ECR

* **Create an ECR repository**

```
aws ecr create-repository \
  --repository-name h2o \
  --profile ming_ecr \
  --region us-east-2
```

* **Authenticate Docker to use ECR registry**

```
aws2 ecr get-login --region us-east-2 --no-include-email --profile ming_ecr
```

The output of the above command is the command to login Docker, which should look like this:

```
docker login -u AWS -p [PASSWORD] https://[AWS_ACCOUNT_ID].dkr.ecr.us-east-1.amazonaws.com
```

The the output as a command to authenticate Docker

* **Tag image to ECR RepositoryUri**

```
docker tag h2o:base [AWS_ACCOUNT_ID].dkr.ecr.us-east-2.amazonaws.com/h2o:base
```

* **Push image to ECR**

```
docker push [AWS_ACCOUNT_ID].dkr.ecr.us-east-2.amazonaws.com/h2o:base
```

## Create S3 Bucket

Regions outside of `us-east-1` require the appropriate **LocationConstraint** 
to be specified in order to create the bucket in the desired region

```
aws s3api create-bucket \
    --acl private 
    --profile ming_s3 
    --region us-east-2 
    --bucket sagemaker-h2o-experiments 
    --create-bucket-configuration LocationConstraint=us-east-2
```
