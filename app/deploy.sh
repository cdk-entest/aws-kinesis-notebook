zip myapp.zip application_properties.json streaming-file-sink.py flink-sql-connector-kinesis-1.15.2.jar
aws s3 cp myapp.zip s3://data-lake-demo-17072023/code/zeppelin-code/myapp_v4.zip