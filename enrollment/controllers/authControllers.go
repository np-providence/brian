package controllers

import (
  "net/http"
  "../models"
  u "../utils"
)

var CreateAttendee = func(w http.ResponseWriter, r *http.Request){
  attendee := &models.Attendee{}
  resp := attendee.Create()
  u.Respond(w, resp)
}

