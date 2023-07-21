# haimtran 21/07/2023
# get record from a stream 
import boto3
import time 
from concurrent.futures import ThreadPoolExecutor

# parameterse 
REGION = "ap-southeast-1"
STREAM_NAME = "stock-input-stream"
NUM_CONSUMER = 5

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
        response = client.get_records(
            ShardIterator = shard_iterator, 
            Limit=10
        )
        # record
        records = response["Records"]
        # next iterator 
        shard_iterator = response["NextShardIterator"]
        print(records)
        record_count += len(records)
        time.sleep(1)


# multiple consumer 
def multi_consumer():
    """
    multiple consumer 
    """
    with ThreadPoolExecutor(max_workers=NUM_CONSUMER) as executor:
        for k in range(1, NUM_CONSUMER):
            executor.submit(get_records())


if __name__=="__main__":
    # get_records()
    multi_consumer()