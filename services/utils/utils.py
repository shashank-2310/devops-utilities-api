import boto3
import botocore.exceptions
from datetime import datetime, timezone


#Validate credentials by making a lightweight STS call
def _validate_creds(session):
    try:
        sts = session.client("sts")
        sts.get_caller_identity()
    
    except botocore.exceptions.NoCredentialsError:
        raise RuntimeError("AWS credentials not found. Configure credentials or set environment variables.")
    
    except botocore.exceptions.ClientError as e:
        raise RuntimeError(f"AWS client error during credential check: {e}")
    
    except Exception as e:
        raise RuntimeError(f"Unexpected error while checking credentials: {e}")


#Establish boto3 session and Get current date and time
def _get_session_and_date():
    session = boto3.Session()
    _validate_creds(session)

    current_datetime = datetime.now(timezone.utc)
    return session, current_datetime


#Fetch all S3 buckets
def _s3_utility():
    session, current_datetime = _get_session_and_date()
    s3 = session.client("s3")
    
    buckets = s3.list_buckets().get("Buckets", [])

    return buckets, current_datetime

