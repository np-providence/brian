package models
import(
  u "../utils"
)

type Feature struct{
  HashFeature string `gorm:"primary_key"`
  AttendeeID string `json:"attendee_id"`
  EventOwnerID string `json:"eventowner_id"`
  FaceFeature string `json:"face_feature"`
}

func (feature *Feature) Create() (map[string] interface{}){
  GetDB().Create(feature)
  response := u.Message(true, "Feature has been created")
  response["feature"] = feature
  return response
}
