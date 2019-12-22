import sagemaker
from sagemaker.processing import ScriptProcessor, ProcessingInput, ProcessingOutput
import boto3
import os

# create a sagemaker session for ScriptProcessor
os.environ['AWS_PROFILE'] = 'ming_sagemaker'
sm_client = boto3.client('sagemaker', region_name='us-east-2')
sm_session = sagemaker.Session(sagemaker_client=sm_client)

# Create a Processor
script_processor = ScriptProcessor(
    command=['python3', '-v'],
    image_uri='261319253434.dkr.ecr.us-east-2.amazonaws.com/h2o:base',
    role='[SAGEMAKER_ROLE]',
    instance_type='ml.m5.xlarge',
    instance_count=1,
    sagemaker_session=sm_session,
)

inputs = [
    ProcessingInput(
        input_name='raw_data',
        source='s3://sagemaker-h2o-experiments/VSQMortality_20190302',
        destination='/opt/ml/processing/input/raw_data'
    )
]

outputs = [
    ProcessingOutput(
        output_name='output',
        source='/opt/ml/processing/output',
        destination='s3://sagemaker-h2o-experiments/output',
    )
]

# run script
script_processor.run(
    code='data_manipulation.py',
    inputs=inputs,
    outputs=outputs,
    arguments=[
        '--raw-data', '/opt/ml/processing/input/raw_data/VSQMortality_20190320a.csv'
    ]
)
