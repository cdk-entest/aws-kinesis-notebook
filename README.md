---
author: haimtran
title: getting started with kinesis data analytics
description:
publishedDate: 17/07/2023
date: 17/07/2023
---

## Introduction

This [GitHub]() shows

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

## Reference

- [query with kda](https://aws.amazon.com/blogs/big-data/query-your-data-streams-interactively-using-kinesis-data-analytics-studio-and-python/)

- [introduction to kda studio and application](https://aws.amazon.com/blogs/aws/introducing-amazon-kinesis-data-analytics-studio-quickly-interact-with-streaming-data-using-sql-python-or-scala/?sc_channel=EL&sc_campaign=Demo_Deep_Dive_2021_vid&sc_medium=YouTube&sc_content=Video9639&sc_detail=ANALYTICS&sc_country=US)

- [apache flink timely stream processing](https://nightlies.apache.org/flink/flink-docs-release-1.14/docs/concepts/time/)

- [apache flink window](https://flink.apache.org/2015/12/04/introducing-stream-windows-in-apache-flink/)
