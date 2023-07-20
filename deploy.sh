zip -r Hello.zip kda-app/
aws s3 cp Hello.zip s3://data-lake-demo-17072023/debug/zeppelin-code/