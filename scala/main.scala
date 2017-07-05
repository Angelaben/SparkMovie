package test.lol

import test.lol.MovieUtils._
//import test.lol.NewFile

import org.apache.spark.{SparkConf, SparkContext}
import org.apache.spark.rdd._

object Main {
  def main(args: Array[String]): Unit = {
    val path = "parsed.txt"

    agreg(path)
  }

  def agreg(path: String): RDD[Movie] = {
    val conf = new SparkConf().setAppName("SparkMovie")
                              .setMaster("local[*]")

    val sc = SparkContext.getOrCreate(conf)

    val lines = sc.textFile(path)
                  .flatMap(StringToMovie)

    lines.foreach(println)
   // lines.saveAsTextFile("out/")
  //  lines.foreach(e => println(e.id))
    sc.stop()
    return lines
  }
  //counts.saveAsTextFile("data/wordcountresult.txt")
}
