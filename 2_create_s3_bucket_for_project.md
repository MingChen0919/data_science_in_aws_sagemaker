# Create S3 Bucket for Project

Each project should have an individual S3 bucket to store data and project code. **The Bucket name has to start with `sagemaker`**. The recommended bucket name is `sagemaker-[PROJECT-NAME]`. Replace **[PROJECT-NAME]** with actual project name. Bucket name cannot be uppercase and have `_`.

## Create Bucket Command

```
aws2 s3 mb s3://sagemaker-[PROJECT-NAME] --region [REGION_NAME] --profile [S3_ACCESS_PROFILE]
```

[S3_ACCESS_PROFILE] should be stored in your `~/.aws/credential` file.

## Sync Data and Project Code Folders to S3

### Sync Folder to S3

```
aws2 s3 sync --profile [S3_ACCESS_PROFILE] [LOCAL_DIR_PATH] [S3Uri]
```

### Upload file to S3

```
aws2 s3 cp --profile [S3_ACCESS_PROFILE] [LOCAL_FILE_PATH] [S3Uri]
```
