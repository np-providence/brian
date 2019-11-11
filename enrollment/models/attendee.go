package models
import(
  u "../utils"
)

type Attendee struct {
  ID string `gorm:"primary_key"`
  Course string `json:"course"`
  Year string `json:"year"`
  Name string `json:"name"`
  Gender string `json:"gender"`
  Status bool `json:"status"`
  Email string `json:"email"`
}

func (attendee *Attendee) Create() (map[string] interface{}){
  GetDB().Create(attendee)
  response := u.Message(true, "Attendee been created")
  response["attendee"] = attendee
  return response
}

func GetAttendee(u string) (*Attendee, error) {
  att := &Attendee{}
  //GetDB().Table("attendees").Where("email= ?", u).First(att)
  if err := GetDB().Table("attendees").Where("email = ?", u).First(att).Error; err != nil {
    return nil, err
  }
  return att, nil
}
