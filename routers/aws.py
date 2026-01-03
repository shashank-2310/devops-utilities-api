from fastapi import APIRouter, HTTPException
from services.aws_service import get_buckets_info, get_bucket_age_info, get_instances_info

router = APIRouter()

@router.get("/s3", status_code=200)
def get_buckets():
    """
        This API gets the Amazon S3 bucket information:
        - total_buckets: Total number of S3 buckets
        - total_new_buckets: Number of buckets created in the last 90 days
        - total_old_buckets: Number of buckets older than 90 days
        - new_buckets: List of names of new buckets
        - old_buckets: List of names of old buckets
    """

    try:
        buckets = get_buckets_info()
        return buckets
    except:
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error"
        )


@router.get("/s3/analysis", status_code=200)
def get_bucket_age_analysis():
    """
        This API gets the Amazon S3 bucket age analysis:
        - BucketName: Name of S3 bucket
        - Age: Age of bucket in days
        - AgeCategory: Category based on bucket age (<30 days, 30-180 days,...etc)
        - CreationDate: Creation date of bucket
    """ 

    try:
        buckets = get_bucket_age_info()
        return buckets
    except:
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error"
        )


@router.get("/ec2", status_code=200)
def get_instances():
    """
        This API gets the Amazon EC2 instance information:
        - total_instances: Total number of EC2 instances
        - running_instances: Number of running instances
        - stopped_instances: Number of stopped instances
        - instance_ids: List of all instance IDs
        - running_instances_info: Detailed info of running instances
        - stopped_instances_info: Detailed info of stopped instances
    """

    try:
        instances = get_instances_info()
        return instances
    except:
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error"
        )