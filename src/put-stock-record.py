# %flink.ipyflink
import datetime
import json
import random
import boto3
import time 
import math


STREAM_NAME = "input-stream"
REGION = "ap-southeast-1"

def get_data_sin(i):
    i = int(math.remainder(i, 4))
    names = ["BTC","ETH","BNB", "XRP", "DOGE"]
    price = 10 + round(100 * math.sin(2 * math.pi * i / 4.0))
    event_time = datetime.datetime.now().isoformat()
    return {
        'event_time': event_time, 
        'ticker': names[i], 
        'price': price
    }


def get_data():
    return {
        'event_time': datetime.datetime.now().isoformat(),
        'ticker': random.choice(["BTC","ETH","BNB", "XRP", "DOGE"]),
        'price': round(random.random() * 100, 2)}


def generate(stream_name, kinesis_client):
    i = 0
    while True:
        data = get_data()
        print(data)
        kinesis_client.put_record(
            StreamName=stream_name,
            Data=json.dumps(data),
            PartitionKey="partitionkey")
        # time.sleep(1)
        i = i + 1


if __name__ == '__main__':
    generate(STREAM_NAME, boto3.client('kinesis', region_name=REGION))