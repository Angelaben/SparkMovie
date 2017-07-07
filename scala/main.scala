package test.lol

import test.lol.MovieUtils._
//import test.lol.NewFile

import org.apache.kafka.common.serialization.StringDeserializer
import org.apache.kafka.clients.consumer.KafkaConsumer
import org.apache.spark.{SparkConf, SparkContext}
import org.apache.spark.rdd._
import scala.collection.JavaConverters._
import java.util.{Collections, Properties}

object Main {
  def main(args: Array[String]): Unit = {
    // Start kafka consumer
    val properties = new Properties()
    properties.put("bootstrap.servers", "localhost:9092")
    properties.put("group.id", "yyuhr@")
    properties.put("key.deserializer", classOf[StringDeserializer])
    properties.put("value.deserializer", classOf[StringDeserializer])
    properties.put("partition.assignment.strategy", "range")

    val kafkaConsumer = new KafkaConsumer[String, String](properties)
    kafkaConsumer.subscribe("my-topic")

    // Create spark context
//    val conf = new SparkConf().setAppName("SparkMovie")
//                              .setMaster("local[*]")
//    val sc = SparkContext.getOrCreate(conf)

    var lines = ""
    while (true) {
      val result = kafkaConsumer.poll(2000).asScala
      for ((topic, data) <- result) {
      
        println(data.getClass)
        /*
        lines = sc.textFile(data)
                  .flatMap(StringToMovie)
      
        lines.foreach(println)
        lines.saveAsTextFile("out/")
        */
      }
    }
  //  lines.foreach(e => println(e.id))
  // sc.stop()
   // }
  }

}
