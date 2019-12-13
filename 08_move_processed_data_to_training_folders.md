# Move Processed Data to Training Folders

At this step you have have data in `s3://PROJECT_NAME/processing/input` and/or `s3://PROJECT_NAME/processing/output` ready for model training.

## Sync Data Folders

```
aws2 s3 sync --profile [S3_ACCESS_PROFILE] s3://PROJECT_NAME/processing/input/FOLDER_1 s3://PROJECT_NAME/input/data/training/input/FOLDER_1

aws2 s3 sync --profile [S3_ACCESS_PROFILE] s3://PROJECT_NAME/processing/input/FOLDER_1 s3://PROJECT_NAME/input/data/validation/input/FOLDER_1

aws2 s3 sync --profile [S3_ACCESS_PROFILE] s3://PROJECT_NAME/processing/input/FOLDER_1 s3://PROJECT_NAME/input/data/testing/input/FOLDER_1
```

## Copy One File to Another Path

`aws2 s3 sync` only works for directories. We need `aws2 s3 cp` to copy a file from one S3Uri to another S3Uri.
