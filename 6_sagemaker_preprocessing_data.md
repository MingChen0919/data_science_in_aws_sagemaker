# Preprocessing Data With Sagemaker

**To make sagemaker to work, the S3 Bucket name needs to start with `sagemaker`!!!**

I don't like launching a Sagemaker Notebook Instance to run my code, because launching a Notebook Instance causes extra cost, and I like code in PyCharm instead of Jupyte Notebook.

Below is an example of launch sagemaker completely locally.


```python
import sagemaker
from sagemaker.processing import ScriptProcessor, ProcessingInput, ProcessingOutput
import os
import boto3

# create a sagemaker session for ScriptProcessor
os.environ['AWS_PROFILE'] = 'ming_sagemaker'
sm_client = boto3.client('sagemaker', region_name='us-east-2')
sm_session = sagemaker.Session(sagemaker_client=sm_client)

# Create a Processor
script_processor = ScriptProcessor(
    command=['python3', '-v'],
    image_uri=[IMAGE ECRUri],
    role=[SAGEMAKER ROLE],
    instance_type='ml.m5.xlarge',
    instance_count=1,
    sagemaker_session=sm_session,
)

inputs = [
    ProcessingInput(
        input_name='images_dir',
        source='s3://sagemaker-vqs-sla/inputs/video_01_vframes',
        destination='/opt/ml/processing/input/images_dir',
        s3_data_type='S3Prefix',
        s3_input_mode='File',
    ),
    ProcessingInput(
        input_name='annotations_dir',
        source='s3://sagemaker-vqs-sla/inputs/video_01_vframes_annotations',
        destination='/opt/ml/processing/input/annotations_dir',
        s3_data_type='S3Prefix',
        s3_input_mode='File',
    ),
    ProcessingInput(
        input_name='code_dependencies',
        source='s3://sagemaker-vqs-sla/code',
        destination='/opt/ml/processing/code_dependencies',
        s3_data_type='S3Prefix',
        s3_input_mode='File',
    )
]
outputs = [
    ProcessingOutput(
        output_name='annotation.json',
        source='/opt/ml/processing/output',
        destination=s3://sagemaker-vqs-sla/preprocessing/output,
    )
]

# Run processing script
script_processor.run(
    code='./code/cli_parse_annotation_files.py',
    inputs=inputs,
    outputs=outputs,
    arguments=[
        '--images_dir', '/opt/ml/processing/input/images_dir',
        '--annotations_dir', '/opt/ml/processing/input/annotations_dir',
        '--annotation_out', '/opt/ml/processing/output/annotation.json'
    ]
)

```

## How Sagemaker Works?

The above code simply translate your script into one command line code and runs it in the specified Docker container in a specified EC2 instance

**command=['python3', '-v'] + code + arguments**

The full version is:

```
python3 -v /opt/ml/processing/input/code/cli_parse_annotation_files.py \
    --images_dir', '/opt/ml/processing/input/images_dir \
    --annotations_dir', '/opt/ml/processing/input/annotations_dir \
    --annotation_out', '/opt/ml/processing/output/annotation.json 
```


Assuming all the paths are correct, Sagemaker will take care of the data transfer between the Docker container and S3.


## How the preprocessing script `.code/cli_parse_annotation_files.py` gets into the Docker container?

When you specify `code='./code/cli_parse_annotation_files.py'` in **script_processor.run**, this code file is automatically uploaded to S3. Sagemaker will automatically creates a `ProcessingInput` object to transfer the file to `/opt/ml/processing/input/code`. Therefore, `/opt/ml/processing/input/code` is a reserved `ProcessingInput` **destination**. You should not use it.


## `ProcessingInput`

`ProcessingInput` maps a **FOLDER OR FILE** to a local path in the Docker container. A Sagemaker Processor can have no more than 10 `ProcessingInput`. **You can only map S3Uri data to `/opt/ml/processing` or its subdirectories. Otherwise, it won't be recognizable by Sagemaker.**


If running the code `./code/cli_parse_annotation_files.py` depends on other python files, the solution is to map those files from S3Uri to a director in `/opt/ml/processing/`, and then add the directory path to the python search paths. 
```
ProcessingInput(
    input_name='code_dependencies',
    source='s3://sagemaker-vqs-sla/code',
    destination='/opt/ml/processing/code_dependencies',
    s3_data_type='S3Prefix',
    s3_input_mode='File',
)
```

To add the dependent python files, you add the following code **at the very beginning of your `./code/cli_parse_annotations.py`**

```
import sys

sys.path.insert(0, "/opt/ml/processing/code_dependencies")
```


## `ProcessingOutput`

`ProcessingOutput` maps a local path in the Docker container to a **FOLDER OR FILE** in S3. Your `./code/cli_parse_annotation_files.py` send outputs to `source` (in this case it is `/opt/ml/processing/output`), then sagemaker transfer the data in the Docker container to `destination` in S3 (in this case it is `s3://sagemaker-vqs-sla/preprocessing/output`).

```
ProcessingOutput(
        output_name='annotation.json',
        source='/opt/ml/processing/output',
        destination=s3://sagemaker-vqs-sla/preprocessing/output,
    )
```
