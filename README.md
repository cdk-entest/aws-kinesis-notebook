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
