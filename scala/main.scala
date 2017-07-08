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
object Main {
  def main(args: Array[String]): Unit = {
    println("======================================" +
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

}
