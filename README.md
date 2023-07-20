---
author: haimtran
title: getting started with kinesis data analytics
description:
publishedDate: 17/07/2023
date: 17/07/2023
---

## Introduction

This [GitHub]() shows

- kinesis cli and producer
- develop with kinesis studio zeppeline notebook
- develop and deploy kda app
- some key concepts of data streaming with flink

## Develop App

- project structure
- configuration
- iam role
- tumbling window

Project structure

```
|--app
   |--application_properties.json
   |--streaming-file-sink.py
   |--deploy.sh
```

Follow this [docs](https://docs.aws.amazon.com/kinesisanalytics/latest/java/examples-python-s3.html) to create configuration for the app

```json
[
  {
    "PropertyGroupId": "consumer.config.0",
    "PropertyMap": {
      "input.stream.name": "stock-input-stream",
      "aws.region": "ap-southeast-1",
      "scan.stream.initpos": "LATEST"
    }
  },
  {
    "PropertyGroupId": "kinesis.analytics.flink.run.options",
    "PropertyMap": {
      "python": "streaming-file-sink.py",
      "jarfile": "flink-sql-connector-kinesis-1.15.2.jar"
    }
  },
  {
    "PropertyGroupId": "sink.config.0",
    "PropertyMap": {
      "output.bucket.name": "data-lake-demo-17072023"
    }
  },
  {
    "PropertyGroupId": "producer.config.0",
    "PropertyMap": {
      "output.stream.name": "stock-output-stream",
      "shard.count": "1",
      "aws.region": "ap-southeast-1"
    }
  }
]
```

Let double check the iam role attached to the flink job. Here is trusted policy

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "kinesisanalytics.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

Permissions for demo purpose

```
CloudWatchFullAccess
CloudWatchLogsFullAccess
AmazonKinesisFullAccess
AmazonS3FullAccess
```

Finally here is the logical code for sink table writting to S3

```py
def create_sink_table(table_name, bucket_name):
    return """ CREATE TABLE {0} (
                ticker VARCHAR(6),
                price DOUBLE,
                event_time TIMESTAMP(3)
              )
              PARTITIONED BY (ticker)
              WITH (
                  'connector'='filesystem',
                  'path'='s3a://{1}/',
                  'format'='json',
                  'sink.partition-commit.policy.kind'='success-file',
                  'sink.partition-commit.delay' = '1 min'
              ) """.format(table_name, bucket_name)

```

Insert to the sink table

```py
table_result = table_env.execute_sql(
    "INSERT INTO {0} SELECT * FROM {1}"
    .format(output_table_name, input_table_name))
```

Simple put data to the stock-input-stream to test output in s3

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
        'ticker': random.choice(['AAPL', 'AMZN', 'MSFT', 'INTC', 'TBV']),
        'price': round(random.random() * 100, 2)	}


def generate(stream_name, kinesis_client):
    while True:
        data = get_data()
        print(data)
        kinesis_client.put_record(
            StreamName=stream_name,
            Data=json.dumps(data),
            PartitionKey="partitionkey")
        time.sleep(1)


if __name__ == '__main__':
    generate(STREAM_NAME, boto3.client('kinesis', region_name = REGION))
```

## Kinesis CLI

aws kinesis get-shard-iterator --shard-id shardId-000000000000 --shard-iterator-type TRIM_HORIZON

```bash
aws kinesis get-shard-iterator \
    --stream-name input-stream \
    --shard-id shardId-000000000001 \
    --shard-iterator-type LATEST
```

Get Records

```bash
aws kinesis get-records \
    --shard-iterator AAAAAAAAAAGQSzIrfkjBufIU6bUR0UXRSoPbPPp0TWaau6wKZgoFArI+lFmGXr3Z2myZwGqUmD/3sWjUXSTYvVCv+dFfu+06g/C0Jmbnzno0FuNI9a2rK+OFTYH0+61fa6efOR4xv3XdVbrzNwT1dJXV4/BGvz0x2GtOh4Go6EUbwcgpL5xdkzjkaT+sg2kBwnfjxTSFkPP/mp7ZkSyc3rU6EOLhLoG1q+CZZJfGX2Oi1ZayHMqcBQ==
```

Enhanced Fan-Out

```bash
aws kinesis register-stream-consumer \
--stream-arn arn:aws:kinesis:ap-southeast-1:681505416554:stream/taxi-stream \
--consumer-name HelloConsumer
```

## Conda Environment

First download miniconda from [here]https://repo.anaconda.com/miniconda/Miniconda3-py39_23.5.2-0-Linux-x86_64.sh, then install miniconda

```bash
bash Miniconda3-latest-Linux-x86_64.sh
```

Create environment

```bash
conda create -n my-new-environment pip python=3.8
```

List environment

```bash
conda infor --envs
```

Activate environment

```bash
conda activate my-new-environment
```

## Reference

- [query with kda](https://aws.amazon.com/blogs/big-data/query-your-data-streams-interactively-using-kinesis-data-analytics-studio-and-python/)

- [introduction to kda studio and application](https://aws.amazon.com/blogs/aws/introducing-amazon-kinesis-data-analytics-studio-quickly-interact-with-streaming-data-using-sql-python-or-scala/?sc_channel=EL&sc_campaign=Demo_Deep_Dive_2021_vid&sc_medium=YouTube&sc_content=Video9639&sc_detail=ANALYTICS&sc_country=US)

- [apache flink timely stream processing](https://nightlies.apache.org/flink/flink-docs-release-1.14/docs/concepts/time/)

- [apache flink window](https://flink.apache.org/2015/12/04/introducing-stream-windows-in-apache-flink/)

- [apache flink connector and checkpoint](https://nightlies.apache.org/flink/flink-docs-master/docs/connectors/table/filesystem/)

- [kineis shard limit](https://docs.aws.amazon.com/streams/latest/dev/service-sizes-and-limits.html)

- [kinesis flink query](https://aws.amazon.com/blogs/big-data/top-10-flink-sql-queries-to-try-in-amazon-kinesis-data-analytics-studio/)

- [kinesis flink write to s3 docs](https://docs.aws.amazon.com/kinesisanalytics/latest/java/examples-python-s3.html)

- [flink window](https://nightlies.apache.org/flink/flink-docs-master/docs/dev/datastream/operators/windows/)

- [flink event time and watermark](https://nightlies.apache.org/flink/flink-docs-master/docs/concepts/time/#event-time-and-watermarks)

- [flink event and watermak 1](https://www.youtube.com/watch?v=QVDJFZVHZ3c)

- [flink event and watermak 2](https://www.youtube.com/watch?v=sdhwpUAjqaI&list=LL&index=3)
