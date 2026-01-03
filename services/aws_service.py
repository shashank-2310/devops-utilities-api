import boto3
import botocore.exceptions
from datetime import datetime, timezone, timedelta


def _validate_creds(session):
    #Validate credentials by making a lightweight STS call
    try:
        sts = session.client("sts")
        sts.get_caller_identity()
    
    except botocore.exceptions.NoCredentialsError:
        raise RuntimeError("AWS credentials not found. Configure credentials or set environment variables.")
    
    except botocore.exceptions.ClientError as e:
        raise RuntimeError(f"AWS client error during credential check: {e}")
    
    except Exception as e:
        raise RuntimeError(f"Unexpected error while checking credentials: {e}")


def _s3_utility():
    # Establish connection to S3 and fetch all S3 buckets
    # Then get Current date and time
    session = boto3.Session()
    _validate_creds(session)
    
    s3 = session.client("s3")
    buckets = s3.list_buckets().get("Buckets", [])

    current_datetime = datetime.now(timezone.utc)

    return buckets, current_datetime


def get_buckets_info():
    #Get Amazon S3 bucket info 
    buckets, current_datetime = _s3_utility()

    old_buckets = []
    new_buckets = []
    
    for bucket in buckets:
        bucket_name = bucket["Name"]

        creation_date = bucket["CreationDate"]
        days_ago_90 = current_datetime - timedelta(days=90)

        if creation_date < days_ago_90:
            old_buckets.append(bucket_name)
        else:
            new_buckets.append(bucket_name)

    return {
        "total_buckets": len(buckets),
        "total_new_buckets": len(new_buckets),
        "total_old_buckets": len(old_buckets),
        "new_buckets": new_buckets,
        "old_buckets": old_buckets
    }


def get_bucket_age_info():
    #Get S3 bucket age analysis
    buckets, current_datetime = _s3_utility()
    bucket_details = []
    
    def _bucket_age_cat(days):
        if days < 30:
            return "<30 days"
        elif 30 <= days <= 180:
            return "30-180 days"
        elif 180 < days <= 365:
            return "180-365 days"
        else:
            years = days // 365
            return f">{years} years"

    for bucket in buckets:
        bucket_name = bucket['Name']
        creation_date = bucket['CreationDate']
        age = (current_datetime - creation_date).days
        age_cat = _bucket_age_cat(age)
        data = {
            "BucketName": bucket_name,
            "AgeDays": age,
            "AgeCategory": age_cat,
            "CreationDate": creation_date.strftime("%Y-%m-%d")
        }
        bucket_details.append(data)

    return bucket_details
    

def get_instances_info():
    #Get Amazon EC2 instance info
    session = boto3.Session()
    _validate_creds(session)
    ec2 = session.client("ec2")

    paginator = ec2.get_paginator("describe_instances")

    running_instances = []
    stopped_instances = []
    other_instances = []

    for page in paginator.paginate():
        for reservation in page.get("Reservations", []):
            for instance in reservation.get("Instances", []):
                tags = {tag.get('Key'): tag.get('Value') for tag in instance.get('Tags', [])}
                launch_time = instance.get('LaunchTime')

                data = {
                    "id": instance.get('InstanceId', "N/A"),
                    "name": tags.get('Name', 'N/A'),
                    "type": instance.get('InstanceType', "N/A"),
                    "az": instance.get('Placement', {}).get('AvailabilityZone', "N/A"),
                    "state": instance.get('State', {}).get('Name', "N/A"),
                    "private_ip": instance.get('PrivateIpAddress'),
                    "public_ip": instance.get('PublicIpAddress'),
                    "subnet_id": instance.get('SubnetId'),
                    "vpc_id": instance.get('VpcId')
                }

                state = (data.get('state') or '').lower()
                if state == 'running':
                    if launch_time:
                        try:
                            now = datetime.now(timezone.utc).astimezone()
                            started = launch_time.astimezone()
                            delta = now - started
                        except Exception:
                            try:
                                delta = datetime.now(timezone.utc).astimezone() - launch_time
                            except Exception:
                                delta = None

                        if delta is not None:
                            data["running_duration"] = str(delta)
                        else:
                            data["running_duration"] = None
                    else:
                        data["running_duration"] = None

                    running_instances.append(data)
                elif state == 'stopped':
                    stopped_instances.append(data)
                else:
                    other_instances.append(data)

    total = len(running_instances) + len(stopped_instances) + len(other_instances)

    return {
        "total_instances": total,
        "running_count": len(running_instances),
        "stopped_count": len(stopped_instances),
        "other_count": len(other_instances),
        "running_instances": running_instances,
        "stopped_instances": stopped_instances,
        "other_instances": other_instances
    }
