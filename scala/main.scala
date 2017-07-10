package test.lol
import test.lol.AlloUtils
import test.lol.MovieUtils._
import test.lol.RatingUtils._
//import test.lol.NewFile
import scala.collection.JavaConversions._
import org.apache.kafka.common.serialization.StringDeserializer
import org.apache.spark.{SparkConf, SparkContext}
import org.apache.spark.rdd._
import scala.collection.JavaConverters._
import java.util.{Collections, Properties}
import java.io._
import kafka.message._
import kafka.serializer._
import kafka.utils._
import java.util.Properties
import kafka.utils.Logging
import scala.collection.JavaConversions._
import java.util
import org.apache.hadoop.io._
import org.apache.hadoop.mapreduce.lib.output.TextOutputFormat
import org.apache.hadoop.fs.FileSystem
import org.apache.kafka.clients.consumer.{ConsumerConfig, KafkaConsumer, ConsumerRecord}
import org.apache.kafka.clients.consumer
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
    topics.add("my-ratings")
    consumer.subscribe(topics)
  }

  def toBeginning() = {
    val top = new util.ArrayList[TopicPartition]()
    top.add(new TopicPartition("my-ratings", 2))
    consumer.seekToBeginning(top)
  }

  def Toshow() = {
    println("Show")
    val conf = new SparkConf().setAppName("testdelamortquitue").setMaster("local[*]")
    val sc = SparkContext.getOrCreate(conf)

   new File("testFile.txt").delete()
   while (true) {
     var hasWritten = false
     var fileWriter = new FileWriter("testFile.txt", true)
     println("Listening - scala ")

     val records = consumer.poll(1000)
     var text = ""
     //val it = records.records("my-topic").iterator()
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

     if (new File("testFile.txt").length() != 0 && hasWritten == true) {
       println ("parsing:")
       val rdd = sc.textFile("testFile.txt")
         .flatMap(AlloUtils.StringToAllo)
       //rdd.saveAsTextFile("hdfs")
       rdd.repartition(1).saveAsTextFile("hdfs" + rdd.hashCode())
         println("GOOD")
     }


   }
  }

  def main(args: Array[String]): Unit = {
    println("babidoo")
    start()
    //toBeginning()
    Toshow()
  }

}
