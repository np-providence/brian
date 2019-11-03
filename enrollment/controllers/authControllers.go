package controllers

import (
  "net/http"
  "../models"
  u "../utils"
  "fmt"
  "strconv"
  "encoding/json"
)

var CreateAttendee = func(w http.ResponseWriter, r *http.Request){
  attendee := &models.Attendee{}
  // Decodes data from r.Body and write the data into attendee 
  err := json.NewDecoder(r.Body).Decode(attendee)
  if err != nil {
    u.Respond(w, u.Message(false, "Invalid request"))
    return
  }
  resp := attendee.Create()
  u.Respond(w, resp)
}


var GetAttendeeFor = func(w http.ResponseWriter, r *http.Request){
  query := r.FormValue("id")
  id64 , err:= strconv.ParseUint(query, 10, 64)
  id := uint(id64)
  if err != nil {
    fmt.Println("THIS IS WRONG")
    return
  }
  data := models.GetAttendee(id)
  resp := u.Message(true, "success")
  resp["data"] = data
  u.Respond(w, resp)
}

