package models
import(
  u "../utils"
)

type EventOwner struct{
  EventOwnerID string `gorm:"primary_key" json:"eventowner_id"`
  Name string `json:"name"`
  Gender string `json:"gender"`
  Status bool `json:"status"`
}

func (eventowner *EventOwner) Create() (map[string] interface{}){
  GetDB().Create(eventowner)
  response := u.Message(true, "Event Owner has been created")
  response["eventowner"] = eventowner
  return response
}

func GetEventOwner(u uint) (*EventOwner){
  evntown := &EventOwner{}
  GetDB().Table("event_owners").Where("eventowner_id = ?", u).First(evntown)
  return evntown
}
