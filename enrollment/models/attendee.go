package models
import(
  "github.com/jinzhu/gorm"
  u "../utils"
)

type Attendee struct {
  gorm.Model
  Course string `json:"course"`
  Year string `json:"year"`
  Name string `json:"name"`
  Images string `json:"images"`
  Gender string `json:"gender"`
}

func (attendee *Attendee) Create() (map[string] interface{}){
  GetDB().Create(attendee)
  response := u.Message(true, "Attend been created")
  response["attendee"] = attendee
  return response
}
