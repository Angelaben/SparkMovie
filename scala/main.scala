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
      props.put(ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG, "org.apache.kafka.common.serialization.StringDeserializer")
      props.put(ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG, "org.apache.kafka.common.serialization.StringDeserializer")
      props.put("partition.assignment.strategy", "org.apache.kafka.clients.consumer.RangeAssignor")
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
      while (true) {
        println("Listening - scala ")
        val records = consumer.poll(1000)
        val it = records.records("my-topic").iterator()
        while (it.hasNext) {
          val record = it.next()
          println("Message reçu : " + record.value())
        }
        Thread.sleep(2000)
      }
    }
    def main(args: Array[String]): Unit = {
      println("beboop")
      start()
      //toBeginning()
      Toshow()
    }

  }
  //def main(args: Array[String]): Unit = {


  /*  println("======================================" +
      "Lancement askip" +
      "===========================================")
    // Start kafka consumer
    val properties = new Properties()
    properties.put("bootstrap.servers", "localhost:9092")
    properties.put("group.id", "peperoni")
    properties.put("zookeeper.connect", "localhost:2181")
    properties.setProperty("zookeeper.connect", "localhost:2181")

    properties.put("key.deserializer", classOf[StringDeserializer])
    properties.put("value.deserializer", classOf[StringDeserializer])
    properties.put("partition.assignment.strategy", "range")
    val kafkaConsumer = new KafkaConsumer[String, String](properties)
    kafkaConsumer.subscribe("my-topic")
    /*************        ****************/
    val props = new Properties()

    props.put("zookeeper.connect", "localhost:2181")

    val config = new ConsumerConfig(props)
    val connector = Consumer.create(config)
    val stream = connector.createMessageStreamsByFilter("my-topic", 1, new StringDecoder(null), new StringDecoder(null))(0)
    val it = stream.iterator()
    while(it.hasNext()) {
      println("REPONSE : " + it.next().message())
    }
    /*************    *********************/
    // Create spark context
    val conf = new SparkConf().setAppName("SparkMovie")
      .setMaster("local[*]")
    val sc = SparkContext.getOrCreate(conf)

    var lines = ""
    //  while (true) {
    val records = kafkaConsumer.poll(1)
    println("================"+records)
    //val result = kafkaConsumer.poll(2000).asScala

    //for ((topic, data) <- result) {

//    println(data.getClass)
    /*
    lines = sc.textFile(data)
              .flatMap(StringToMovie)

    lines.foreach(println)
    lines.saveAsTextFile("out/")
    */
    //   }
    //  }
    //  lines.foreach(e => println(e.id))
    // sc.stop()
    // }
  }
*/

