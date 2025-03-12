# ebs-snapshot-cleanup

## Steps to Deploy in AWS Lambda

1️⃣ Create an IAM Role with permissions:

ec2:DescribeSnapshots

ec2:DeleteSnapshot

ec2:DescribeVolumes

2️⃣ Create a Lambda Function:
Runtime: Python 3.x
Memory: 128 MB (or higher if needed)
Timeout: 30 seconds

3️⃣ Use the following code in the Lambda function:

4️⃣ Set an EventBridge Rule to trigger this function periodically (e.g., every week).

# How It Works in Lambda?

1️⃣ Gets all snapshots owned by the AWS account.

2️⃣ Filters snapshots older than 30 days and not linked to any volume.

3️⃣ Deletes them securely with error handling and logging.