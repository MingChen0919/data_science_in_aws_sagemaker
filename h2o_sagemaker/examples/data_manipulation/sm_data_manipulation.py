import sagemaker
from sagemaker.processing import ScriptProcessor, ProcessingInput, ProcessingOutput
import boto3
import os

# create a sagemaker session for ScriptProcessor
os.environ['AWS_PROFILE'] = 'ming_sagemaker'
sm_client = boto3.client('sagemaker', region_name='us-east-2')
sm_session = sagemaker.Session(sagemaker_client=sm_client)