"""
haimtran 17/07/2023
This is from Lab 2 building streaming data application on aws 
Script to generate clickstream data and send to aws stream.
"""

import json
import random
from datetime import datetime
import sys
import time
import hashlib

import boto3


def get_event_id():
    hashed = hashlib.md5(datetime.now().strftime("%m/%d/%YT%H:%M:%S.%f").encode())

    return hashed.hexdigest()

def get_event():
    events = [
        "purchased_item", "liked_item", "reviewed_item", "entered_payment_method",
        "clicked_review", "clicked_item_description"
    ]

    return random.choice(events)

def get_item_quantity(eventname):
    MAX_ITEM_LIMIT = 5
    if (eventname == 'purchased_item'):
        itemqty=random.randint(1, MAX_ITEM_LIMIT)
    else:
        itemqty=0
    return itemqty

def get_item_id(page_name):
    #print(page_name)
    if (page_name == 'apparel'):
        MIN_ITEM_LIMIT = 11
        MAX_ITEM_LIMIT = 13
    elif (page_name == 'food'):
        MIN_ITEM_LIMIT = 21
        MAX_ITEM_LIMIT = 23
    elif (page_name == 'electronics'):
        MIN_ITEM_LIMIT = 31
        MAX_ITEM_LIMIT = 33
    elif (page_name == 'home'):
        MIN_ITEM_LIMIT = 41
        MAX_ITEM_LIMIT = 43
    else:
        MIN_ITEM_LIMIT = 51
        MAX_ITEM_LIMIT = 53

    #print(MIN_ITEM_LIMIT)
    #print(MAX_ITEM_LIMIT)
    return random.randint(MIN_ITEM_LIMIT, MAX_ITEM_LIMIT)


def get_user_id():
    MAX_USER_ID = 50

    return random.randint(1, MAX_USER_ID)

def get_event_time():
    #return datetime.now().strftime("%m/%d/%YT%H:%M:%S.%f")
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

def get_os():
    os = ["ios", "android", "web"]

    return random.choice(os)

def get_page():
    pages = ["apparel", "food", "electronics", "home", "books"]

    return random.choice(pages)
if __name__ == '__main__':
    print ("\n Number of arguments:", len(sys.argv), "arguments")
    print ("\n Argument List:", str(sys.argv))
    print ("\n The program name is:", str(sys.argv[0]))
    print ("\n The kinesis data stream name is :", str(sys.argv[1]))
    print ("\n Max interval in seconds between records :", str(sys.argv[2]))
    verbose=''
    if (len(sys.argv) > 4) :
        if (str(sys.argv[4]) == '--verbose'):
            print ("\n Verbose  :", str(sys.argv[4]))
            verbose=str(sys.argv[4])

    MAX_SECONDS_BETWEEN_EVENTS = int(sys.argv[3])
    stream_name =str(sys.argv[1])
    my_session = boto3.session.Session()
    y_region = my_session.region_name
    client = my_session.client("kinesis")

    while True:

        delay = random.randint(0, MAX_SECONDS_BETWEEN_EVENTS)
        time.sleep(delay)
        eventname=get_event()
        pagename=get_page()

        itemid=get_item_id(pagename)
        itemquantity=get_item_quantity(eventname)

        event = {
            "event_id": get_event_id(),
            "event": eventname,
            "user_id": get_user_id(),
            "item_id": itemid,
            "item_quantity": itemquantity,
            "event_time": get_event_time(),
            "os": get_os(),
            "page": get_page(),
            "url": "www.example.com"
           }

        if (len(verbose) > 0) :
            data = json.dumps(event,indent=1)
        else:
            data = json.dumps(event)
        print(data)
        encoded_data = data.encode("utf-8")
        #stream_name="qls-188082-97e52ead37fe76db-KdsSensorData-lL0cwIdoUClZ"

        response = client.put_record(
            StreamName=stream_name,
            Data=encoded_data,
            PartitionKey="partitionkey")


        if (len(verbose) > 0) :
            print("Message written to the Kineis Data Stream")
            print(json.dumps(response,indent=1))

            print(response["ShardId"])
            print("SequenceNumber:")
            print(response["SequenceNumber"])
            print("HTTStatusCode:")
            print(response["ResponseMetadata"]["HTTPStatusCode"])