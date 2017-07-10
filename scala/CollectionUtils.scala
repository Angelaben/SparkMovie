package scala.movie

import play.api.libs.json.{JsError, JsSuccess, Json}

object CollectionUtils {
  case class Collection(
    id:   Option[Int],
    name: Option[String]
  )

  implicit val collectionFormat = Json.format[Collection]
    
  def StringToCollection(str: String) = {
    Json.parse(str).validate[Collection] match {
    case JsError(e)      => println(e); None
    case JsSuccess(t, _) => Some(t)
    }
  }

}
