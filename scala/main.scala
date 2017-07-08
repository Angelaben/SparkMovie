package test.lol

import test.lol.MovieUtils._
//import test.lol.NewFile
import org.apache.kafka.clients.consumer.ConsumerRecord
import scala.collection.JavaConversions._
import org.apache.kafka.clients.consumer.ConsumerRecords
import org.apache.kafka.common.serialization.StringDeserializer
import org.apache.kafka.clients.consumer.KafkaConsumer
import org.apache.spark.{SparkConf, SparkContext}
import org.apache.spark.rdd._
import scala.collection.JavaConverters._
import java.util.{Collections, Properties}
import kafka.message._
import kafka.serializer._
import kafka.utils._
import org.apache.kafka.clients.consumer
import java.util.Properties
import kafka.utils.Logging
import scala.collection.JavaConversions._
import java.util

import org.apache.kafka.clients.consumer.{ConsumerConfig, KafkaConsumer}
import org.apache.kafka.common.TopicPartition


import java.util.Properties

object Main {
  /**
   * Created by ikuritosensei on 08/07/2017.
   */

  def createConsumerConfig(): Properties = {
    val props = new Properties()
    props.put(ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092")
    props.put(ConsumerConfig.GROUP_ID_CONFIG, "test-consumer-group")
    props.put(ConsumerConfig.ENABLE_AUTO_COMMIT_CONFIG, "true")
    props.put(ConsumerConfig.AUTO_COMMIT_INTERVAL_MS_CONFIG, "1000")
    props.put("zookeeper.connect", "localhost:2181")
    props.put("session.timeout.ms", "30000")
    props.put(ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG,
              "org.apache.kafka.common.serialization.StringDeserializer")
    props.put(ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG,
              "org.apache.kafka.common.serialization.StringDeserializer")
    props.put("partition.assignment.strategy",
              "org.apache.kafka.clients.consumer.RangeAssignor")
    props
  }

  val props = createConsumerConfig()
  val consumer = new KafkaConsumer[String, String](props)

  def start(): Unit = {
    println("Start")
    val topics : util.List[String] = new util.ArrayList[String]()
    topics.add("my-topic")
    consumer.subscribe(topics)
  }

  def toBeginning() = {
    val top = new util.ArrayList[TopicPartition]()
    top.add(new TopicPartition("my-topic", 2))
    consumer.seekToBeginning(top)
  }

  def Toshow() = {
    println("Show")
    val conf = new SparkConf().setAppName("testdelamortquitue").setMaster("local[*]")
    val sc = SparkContext.getOrCreate(conf)
    val test = sc.textFile("reduced-tweets.json")
    println("====================================================================")
    println("====================================================================")
    println(test.getClass())
    // class org.apache.spark.rdd.MapPartitionsRDD

    println("====================================================================")
    println("====================================================================")
    while (true) {
      println("Listening - scala ")
      val records = consumer.poll(1000)
      val it = records.records("my-topic").iterator()
      var fatLine = ""
      while (it.hasNext) {
        val record = it.next()
        println("Message reçu : " + record.value())
        fatLine.concat(record.value)

        val newLine = StringToMovie(record.value())
      //  line.union(newLine)
        println("====================================================================")
        println("type d'objet: " + record.value().getClass)
        println(newLine)
        println("====================================================================")
      }
      Thread.sleep(2000)
  //    var rdd = fatLine.flatMap(StringToMovie)
    }
  }
  def main(args: Array[String]): Unit = {
    println("beboop")
    start()
    //toBeginning()
    Toshow()
  }

}
