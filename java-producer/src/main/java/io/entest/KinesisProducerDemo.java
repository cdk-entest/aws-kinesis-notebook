// haimtran 17/07/2023
// kinesis producer to send data to kinesis stream

package io.entest;

import com.amazonaws.services.kinesis.producer.KinesisProducer;
import com.amazonaws.services.kinesis.producer.KinesisProducerConfiguration;
import org.json.JSONObject;

import java.io.File;
import java.nio.ByteBuffer;
import java.util.List;


public class KinesisProducerDemo {

    public static String streamName = "stock-input-stream";
    public static String region = "ap-southeast-1";

    public static void main(String[] args) throws Exception {
        File tripCsv = new File("data/taxi-trips.csv");

        List<Trip> trips = TripReader.readFile(tripCsv);

        KinesisProducerConfiguration config =
                new KinesisProducerConfiguration().setRecordMaxBufferedTime(3000)
                        .setMaxConnections(1).setRequestTimeout(60000).setRegion(region);

        final KinesisProducer kinesis = new KinesisProducer(config);

        System.out.println(
                "Starting to produce data to " + streamName + " in the " + region + " region.");


        // for (Trip trip: trips) {
        // // System.out.println(trip.id);
        // System.out.println(trip.toString());
        // }

        while (true) {
            for (Trip trip : trips) {
                ByteBuffer data =
                        ByteBuffer.wrap(new JSONObject(trip).toString().getBytes("UTF-8"));
                // doesn't block
                kinesis.addUserRecord(streamName, trip.getId(), data);
            }
        }

    }

}
