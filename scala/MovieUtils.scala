package test.lol


import play.api.libs.json.{JsError, JsSuccess, Json}

object MovieUtils {
  case class Movie(
    id: String,
 //   belongs_to_collection: Collection,
    forAdult: Boolean,
    budget: Int,
  //  genre: List[Genre],
    original_language: String,
    original_title: String,
    overview: String,
    popularity: Float,
    release_date: Int,
    revenue: Int,
    runtime: Int,
    status: String,
    tagline: String,
    title: String,
    vote_average: Float,
    vote_count: Int,
    review: List[String]
  )

  implicit val movieFormat = Json.format[Movie]

  def StringToMovie(str: String) = {
    Json.parse(str).validate[Movie] match {
      case JsError(e)      => println(e); None
      case JsSuccess(t, _) => Some(t)
    }
  }
}
