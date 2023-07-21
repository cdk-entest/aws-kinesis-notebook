---
author: haimtran
title: getting started with kinesis producer
description: getting started with kinesis produce
publishedDate: 17/07/2023
date: 17/07/2023
---

## Install Maven

Let install maven by downloading this binary file and export the path

```bash
wget https://dlcdn.apache.org/maven/maven-3/3.9.3/binaries/apache-maven-3.9.3-bin.tar.gz
```

Update the .bashrch

```bash
export PATH=/home/ec2-user/apache-maven-3.9.3/bin:$PATH
```

## Setup Project

Let create a new java project in vscode using maven

```bash
use vscode to create a new project with maven
```

Project structure

```
|--src
   |--main
      |--java
         |--io
            |--entest
               |--App.java
|--test
  |--java
     |--io
        |--entest
           |App.java
|--target
   |--classes
      |--App.class
```

Let compile the project from the root

```bash
mvn package
```

Then we can run

```bash
java -cp target/amazon-kinesis-replay-1.0-SNAPSHOT.jar io.entest.KinesisProducerDemo
```

## Dependenicies

We can use maven to install dependencies. There are different way to search for pom dependencies such as from vscode or from [this site]

```
<dependency>
    <groupId>com.amazonaws</groupId>
    <artifactId>amazon-kinesis-producer</artifactId>
    <version>0.15.7</version>
</dependency>
```

## Troubleshoting

[this pom.xml](https://github.com/cdk-entest/aws-java-maven/blob/master/pom.xml) works, please double check

## Reference

- [install maven](https://dlcdn.apache.org/maven/maven-3/3.9.3/binaries/apache-maven-3.9.3-bin.tar.gz)

- [maven search](https://central.sonatype.com/artifact/com.amazonaws/amazon-kinesis-producer/0.15.7)

- [kinesis workshop producer](https://catalog.workshops.aws/real-time-streaming-with-kinesis/en-US/lab-1-sdk-ingest/2-kinesis-producer-library/2-1-simple-producer)

- [maven compiler 1.7 lambda error](https://stackoverflow.com/questions/59049980/maven-compiler-release-as-an-replacement-for-source-and-target/65655542#65655542)
