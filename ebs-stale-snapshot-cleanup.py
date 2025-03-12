import boto3
import datetime
import logging

# Setup logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# AWS Configuration
REGION = "us-east-1"  # Change to your AWS region
RETENTION_DAYS = 30  # Number of days before snapshots are considered stale

# Initialize AWS Clients
ec2_client = boto3.client("ec2", region_name=REGION)

def get_stale_snapshots():
    """Fetches EBS snapshots older than the retention period and not attached to any volumes."""
    retention_date = datetime.datetime.utcnow() - datetime.timedelta(days=RETENTION_DAYS)

    try:
        # Fetch all snapshots owned by the account
        snapshots = ec2_client.describe_snapshots(OwnerIds=["self"])["Snapshots"]

        stale_snapshots = []
        for snapshot in snapshots:
            snapshot_id = snapshot["SnapshotId"]
            start_time = snapshot["StartTime"].replace(tzinfo=None)

            # Check if snapshot is older than retention period
            if start_time < retention_date:
                volume_id = snapshot.get("VolumeId", None)
                if not volume_id:  # Only delete snapshots not attached to a volume
                    stale_snapshots.append(snapshot_id)

        return stale_snapshots

    except Exception as e:
        logger.error(f"Error fetching snapshots: {e}")
        return []

def delete_snapshots(snapshot_ids):
    """Deletes the given list of snapshot IDs."""
    if not snapshot_ids:
        logger.info("No stale snapshots found.")
        return

    logger.info(f"Found {len(snapshot_ids)} stale snapshots to delete...")

    for snapshot_id in snapshot_ids:
        try:
            ec2_client.delete_snapshot(SnapshotId=snapshot_id)
            logger.info(f"✅ Deleted snapshot: {snapshot_id}")
        except Exception as e:
            logger.error(f"❌ Failed to delete {snapshot_id}: {e}")

def lambda_handler(event, context):
    """AWS Lambda entry point."""
    logger.info("Starting EBS snapshot cleanup...")
    
    stale_snapshots = get_stale_snapshots()
    delete_snapshots(stale_snapshots)
    
    logger.info("EBS snapshot cleanup completed.")

    return {"statusCode": 200, "body": "Snapshot cleanup executed successfully"}
