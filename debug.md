---
author: haimtran
title: error when two flink jobs on the same kinesis data stream
description:
publishedDate: 17/07/2023
date: 17/07/2023
---

## Introduction

- Create a simple data stream, on-demand
- Put 1 message/second
- Create two simple queries, which means two Flink job
- Then error happen

![hehe](https://github.com/cdk-entest/aws-kinesis-notebook/assets/20411077/240bffc7-d98e-4354-bde4-7ce9e845f7b7)


## Producer

- 1 Kinesis Data Stream, on-demand
- 1 message/second

```py
import datetime
import json
import random
import boto3
import time


STREAM_NAME = "stock-input-stream"
REGION = "ap-southeast-1"


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
            PartitionKey=data["ticker"],
            # PartitionKey="partitionkey"
            )
        time.sleep(1)
        i = i + 1


if __name__ == '__main__':
    generate(STREAM_NAME, boto3.client('kinesis', region_name=REGION))
```

## KDA Studio Notebook

Create a simple table connecting to the stock-input-stream

```sql
%flink.ssql(type='update')
CREATE TABLE stock_table (
    ticker VARCHAR(6),
    price DOUBLE,
    event_time TIMESTAMP(3),
    WATERMARK FOR event_time AS event_time - INTERVAL '5' SECOND)
    PARTITIONED BY (ticker)
    WITH (
    'connector' = 'kinesis',
    'stream' = 'stock-input-stream',
    'aws.region' = 'ap-southeast-1',
    'scan.stream.initpos' = 'LATEST',
    'format' = 'json',
    'json.timestamp-format.standard' = 'ISO-8601')
```

Run a simple query to calculate average stock prive by ticker and window

```sql
%flink.ssql(type=update)
SELECT
        stock_table.ticker as ticker,
        AVG(stock_table.price) AS avg_price,
        TUMBLE_ROWTIME(stock_table.event_time, INTERVAL '10' second) as time_event
FROM stock_table
GROUP BY TUMBLE(stock_table.event_time, INTERVAL '10' second), stock_table.ticker;
```

Run another query or the same query again ==> ERROR happend

```sql
%flink.ssql(type=update)
SELECT
        stock_table.ticker as ticker,
        COUNT(stock_table.ticker) AS ticker_count,
        TUMBLE_ROWTIME(stock_table.event_time, INTERVAL '3' second) as time_event
FROM stock_table
GROUP BY TUMBLE(stock_table.event_time, INTERVAL '3' second), stock_table.ticker;
```

## ERROR

Happen when two Flink jobs running on the same Data Stream. If only one query, one job, then no error. Query can be simple, but 2 queries then error happen

```sql
%flink.ssql(type=update)
SELECT * FROM stock_table;
```
<img width="913" alt="Screenshot 2023-07-21 at 08 56 41" src="https://github.com/cdk-entest/aws-kinesis-notebook/assets/20411077/17b5e7ee-5f8a-49fb-9ac4-400e3891ba65">


