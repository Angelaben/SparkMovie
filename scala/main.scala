package projet.scala.movie

import projet.scala.movie.AlloUtils._
import projet.scala.movie.RatingUtils._

import java.io._
import java.util
import java.util.{Collections, Properties}

import kafka.message._
import kafka.serializer._
import kafka.utils._
import kafka.utils.Logging

import org.apache.kafka.clients.consumer
import org.apache.kafka.clients.consumer.{ConsumerConfig, KafkaConsumer, ConsumerRecord}
import org.apache.kafka.common.TopicPartition
import org.apache.kafka.common.serialization.StringDeserializer
import org.apache.spark.rdd._
import org.apache.spark.{SparkConf, SparkContext}

import scala.collection.JavaConversions._
import scala.collection.JavaConverters._



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
    topics.add("my-ratings")
    consumer.subscribe(topics)
  }

  def toBeginning() = {
    val top = new util.ArrayList[TopicPartition]()
    top.add(new TopicPartition("my-ratings", 2))
    consumer.seekToBeginning(top)
  }

  def toShow(source: String) = {
    println("Show")
    val conf = new SparkConf().setAppName("Movie reviews").setMaster("local[*]")
    val sc = SparkContext.getOrCreate(conf)
    new File("testFile.txt").delete()

    while (true) {
      var hasWritten = false
      var fileWriter = new FileWriter("testFile.txt", true)
      println("Listening - scala ")

      val records = consumer.poll(1000)
      val it = records.records("my-ratings").iterator()
      while (it.hasNext) {
        hasWritten = true
        val record = it.next()
        fileWriter.write(record.value())
        fileWriter.write("\n")
      }

      fileWriter.flush()
      fileWriter.close()
      Thread.sleep(1000)

      if (hasWritten == true && new File("testFile.txt").length() != 0) {
        println ("parsing:")

        if (source == "allo") {
          var rdd = sc.textFile("testFile.txt")
                      .flatMap(StringToAllo)
          rdd.repartition(1).saveAsTextFile("hdfs" + rdd.hashCode())

        }
        else {
          var rdd = sc.textFile("testFile.txt")
                      .flatMap(StringToRating)
          rdd.repartition(1).saveAsTextFile("hdfs" + rdd.hashCode())
        }
        println("GOOD")
      }

    }
  }

    /* USAGE
     * sbt "run arg1"
     * arg1: [ allo | tmdb ]
     */
  def main(args: Array[String]): Unit = {
    if (args.length == 1) {
      start()

      if (args(0) == "allo") {
        println("AlloCiné")
        toShow("allo")
      }
      else if (args(0) == "tmdb") {
        println("TMDB")
        //toBeginning()
        toShow("tmdb")
      }
    }
    else
      println()
      println(" /================================\\")
      println("||                                ||")
      println("|| USAGE                          ||")
      println("||     sbt \"run arg1              ||")
      println("||     arg1: [ allo | tmdb ]      ||")
      println("||                                ||")
      println(" \\================================/")
      println()
  }

}
