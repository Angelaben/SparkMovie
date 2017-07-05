package test.lol


import play.api.libs.json.{JsError, JsSuccess, Json}
import test.lol.GenreUtils._

object MovieUtils {
  case class Movie(
    adult:           Option[Boolean],
 //   belongs_to_collection: Collection,
    budget:             Option[Int],
    genre:              Option[List[Genre]],
    id:                 Option[String],
    original_language:  Option[String],
    original_title:     Option[String],
    overview:           Option[String],
    popularity:         Option[Float],
    release_date:       Option[Int],
    revenue:            Option[Int],
    runtime:            Option[Int],
    status:             Option[String],
    tagline:            Option[String],
    title:              Option[String],
    vote_average:       Option[Float],
    vote_count:         Option[Int],
    review:             Option[List[String]]
  )

  implicit val movieFormat = Json.format[Movie]

  def StringToMovie(str: String) = {
    Json.parse(str).validate[Movie] match {
      case JsError(e)      => println(e); None
      case JsSuccess(t, _) => Some(t)
    }
  }
}
