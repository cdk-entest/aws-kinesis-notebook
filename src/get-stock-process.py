# haimtran 20/07/2023
# multiple consumers reading a shard 
# to see the exceed read throughput error 
import boto3
import os
from multiprocessing import Process
from botocore.exceptions import ClientError
import sys

# parameterse
REGION = "ap-southeast-1"
STREAM_NAME = "stock-input-stream"
NUM_CONSUMER = 10

# kinesis client
client = boto3.client("kinesis", region_name=REGION)

# get records
def get_records(max_records=10000):
    """
    get records from a stream
    """
    response = client.get_shard_iterator(
        StreamName = STREAM_NAME,
        ShardId="shardId-000000000001",
        ShardIteratorType="LATEST"
    )

    # shard interator
    shard_iterator = response["ShardIterator"]

    # get records
    record_count = 0
    while record_count < max_records:
        try:
            response = client.get_records(
            ShardIterator = shard_iterator,
            Limit=10
            )
            # record
            records = response["Records"]
            # next iterator
            shard_iterator = response["NextShardIterator"]
            # print to std out 
            print("id {0} records {1}".format(os.getpid(), records))
            # print to log file 
            record_count += len(records)
            # time.sleep(1)
        except ClientError as error:
            print("================================================ \n")
            print(error)
            print("================================================ \n")
            os.system("pkill -f get-stock-process.py")

if __name__=="__main__":
    # get_records()
    for k in range(1, NUM_CONSUMER):
            Process(target=get_records).start()