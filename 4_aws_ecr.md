# 1. Create a ECR repository to hold project images

* Replace **PROJECT_NAME** with actual project name
* Replace **ECR_ACCESS_PROFILE** with your ECR access credentials stored in `~/.aws/credentials`

```
aws2 ecr create-repository --repository-name PROJECT_NAME --profile ECR_ACCESS_PROFILE
```

# 2. Authenticate Docker to use ECR registry

The goal of this step is to get the login information so the Docker can use ECR, like pushing images to and pulling images from ECR.

* Replace **REGION_NAME** with an actual aws region
* Replace **ECR_ACCESS_PROFILE** with your ECR access credentials stored in `~/.aws/credentials`

```
aws2 ecr get-login --region REGION_NAME --no-include-email --profile ECR_ACCESS_PROFILE
```

The output of the above command is the command to login Docker, which should look like this:

```
docker login -u AWS -p [PASSWORD] https://[AWS_ACCOUNT_ID].dkr.ecr.us-east-1.amazonaws.com
```

# 3. Tag local image to an ECR RepositoryURI

Before we can push an image to an ECR repository, we need to tag the image to the RepositoryURI.

If you have followed the instruction in the previous section, the image you want to push to ECR should have a tag in the format of [PROJECT_NAME]:[FEATURE].


* Replace [PROJECT_NAME]:[FEATURE] with the actual Docker image tag
* We want to add the [FEATURE] of the image to the ERC RepositoryURI

```
docker tag [PROJECT_NAME]:[FEATURE] [AWS_ACCOUNT_ID].dkr.ecr.us-east-2.amazonaws.com/[PROJECT_NAME]:[FEATURE]
```

# 4. Push Image to ECR

Now you can push your image to ECR with command:

```
docker push [AWS_ACCOUNT_ID].dkr.ecr.us-east-2.amazonaws.com/[PROJECT_NAME]:[FEATURE]
```

# Other High-Frequent Actions

## Delete a repository

```
aws2 ecr untag-resource \
  --repository-name [REPOSITORY_NAME] \
  --profile [ECR_ACCESS_PROFILE] \
  --region [REGION]
  --tag-keys [TAG_NAME] 
```

## Remove a tag

```
aws2 ecr untag-resource \
  --resource-arn arn:aws:ecr:[REGION]:[AWS_ACCOUNT_ID]:repository/[REPOSITORY_NAME] \
  --profile [ECR_ACCESS_PROFILE] \
  --region [REGION]
  --tag-keys [TAG_NAME] 
```
