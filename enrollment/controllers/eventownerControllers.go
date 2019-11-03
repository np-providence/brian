package controllers

import (
  "net/http"
  "../models"
  u "../utils"
  "fmt"
  "strconv"
  "encoding/json"
)

var CreateEventOwner = func(w http.ResponseWriter, r *http.Request){
  eventowner := &models.EventOwner{}
  // Decodes data from r.Body and write the data into attendee 
  err := json.NewDecoder(r.Body).Decode(eventowner)
  if err != nil {
    u.Respond(w, u.Message(false, "Invalid request"))
    return
  }
  resp := eventowner.Create()
  u.Respond(w, resp)
}


var GetEventOwnerFor = func(w http.ResponseWriter, r *http.Request){
  query := r.FormValue("eventowner_id")
  id64 , err:= strconv.ParseUint(query, 10, 64)
  id := uint(id64)
  if err != nil {
    fmt.Println(err)
    fmt.Println("THIS IS WRONG")
    return
  }
  data := models.GetEventOwner(id)
  resp := u.Message(true, "success")
  resp["data"] = data
  u.Respond(w, resp)
}
