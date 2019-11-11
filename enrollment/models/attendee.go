package models
import(
  "fmt"
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

func GetAttendee(u uint) (*Attendee) {
  att := &Attendee{}
  fmt.Println(u)
  GetDB().Table("attendees").Where("student_id= ?", u).First(att)
  return att
}
