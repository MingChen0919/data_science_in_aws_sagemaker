# 1. Create a ECR repository to hold project images

* Replace **PROJECT_NAME** with actual project name
* Replace **ECR_ACCESS_PROFILE** with your ECR access credentials stored in `~/.aws/credentials`

```
aws2 ecr create-repository --repository-name PROJECT_NAME --profile ECR_ACCESS_PROFILE
```

