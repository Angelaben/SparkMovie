package projet.scala.movie
import play.api.libs.json._

object AlloUtils  {

  case class Allo (
    title:              String,
    ownRating :         Option[Int],
    director :          Option[String],
    spectators_reviews: Option[String],
    date :              Option[String],
    id :                Option[String]
  ) extends java.io.Serializable

  implicit val movieFormat = Json.format[Allo]

  def StringToAllo(str : String) = Json.parse(str).validate[Allo] match {
    case JsError(e) => println(e); None
    case JsSuccess(t, _) => Some(t)
  }
}
