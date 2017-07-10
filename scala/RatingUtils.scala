package projet.scala.movie

import projet.scala.movie.GenreUtils._
import play.api.libs.json.{JsError, JsSuccess, Json}

object RatingUtils {
  case class Rating(
//    production_countris: Option[Country],
    revenue:             Option[Int],
    overview:            Option[String],
    video:               Option[Boolean],
    id:                  Option[Int],
    genres:              Option[List[Genre]],
    title:               Option[String],
    tagline:             Option[String],
    review:              Option[List[String]],
    vote_count:          Option[Int],
    homepage:            Option[String],
    original_language:   Option[String],
    status:              Option[String],
    imdb_id:             Option[String],
    adult:               Option[Boolean],
    release_date:        Option[String],
    popularity:          Option[Float],
    original_title:      Option[String],
    budget:              Option[Int],
    vote_average:        Option[Float],
    runtime:             Option[Int]
//    production_companies: [{"name": "Miramax Films", "id": 14},
//                           {"name": "A Band Apart", "id": 59}],
  )

  implicit val ratingFormat = Json.format[Rating]

  def StringToRating(str: String) = {
    Json.parse(str).validate[Rating] match {
      case JsError(e)       => println(e); None
      case JsSuccess(t, _) => Some(t)
    }
  }

}
