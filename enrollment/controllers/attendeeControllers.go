package controllers

import (
  "net/http"
  "../models"
  u "../utils"
  "encoding/json"
  "time"
)

var CreateAttendee = func(w http.ResponseWriter, r *http.Request){
  attendee := &models.Attendee{}
  // Decodes data from r.Body and write the data into attendee 
  err := json.NewDecoder(r.Body).Decode(attendee)
  currentTime := time.Now().Local()
  attendee.ID = u.Hash(currentTime.String())
  if err != nil {
    u.Respond(w, u.Message(false, "Invalid request"))
    return
  }
  resp := attendee.Create()
  u.Respond(w, resp)
}


var GetAttendeeFor = func(w http.ResponseWriter, r *http.Request){
  var (resp map[string]interface{})
  query := r.FormValue("email")
  data, err:= models.GetAttendee(query)
  if err != nil {
    resp = u.Message(false, "fail")
    resp["data"] = err
  }else{
    resp = u.Message(true, "success")
    resp["data"] = data
  }
  u.Respond(w, resp)
}
