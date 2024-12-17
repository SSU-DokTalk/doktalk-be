from boto3 import client

from app.core.config import settings

s3_client = client(
    "s3",
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY_ID,
    region_name=settings.AWS_REGION,
)

__all__ = [s3_client]
