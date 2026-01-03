from fastapi import APIRouter, HTTPException
from services.aws_service import get_buckets_info, get_bucket_age_info, get_instances_info, get_cost_and_usage_info

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


@router.get("/s3/analytics", status_code=200)
def get_bucket_age_analysis():
    """
        This API gets the Amazon S3 bucket age analysis:
        - BucketName: Name of the S3 bucket
        - Age: Age of the bucket in days
        - AgeCategory: Age category of the bucket (<30 days, 30-180 days, 180-365 days, >1 year, etc)
        - CreationDate: Creation date of the bucket
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
    

@router.get("/summary", status_code=200)
def get_cost_and_usage():
    """
        This API gets the Amazon Cost and Usage information:
        - from: Start date of the cost analysis period
        - month: Month label of the cost analysis period
        - total_cost: Total cost incurred during the period
        - currency: Currency of the cost values
        - estimated: Indicates if the cost is estimated (bill finalization status)
        - by_service: Breakdown of costs by AWS service
    """

    try:
        cost_and_usage = get_cost_and_usage_info()
        return cost_and_usage
    except:
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error"
        )