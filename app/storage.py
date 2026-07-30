import os

import boto3
from botocore.config import Config
from dotenv import load_dotenv

load_dotenv()

s3_client = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION"),
    config=Config(
        signature_version="s3v4",
        s3={
            "addressing_style": "virtual"
        }
    )
)

