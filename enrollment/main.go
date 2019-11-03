package main

import (
  "github.com/gorilla/mux"
  "os"
  "fmt"
  "net/http"
  "./controllers"
)

func main(){
  router := mux.NewRouter()
  router.HandleFunc("/api/attendee/new", controllers.CreateAttendee).Methods("POST")
  router.HandleFunc("/api/attendee", controllers.GetAttendeeFor).Methods("GET")
  router.HandleFunc("/api/eventowner/new", controllers.CreateEventOwner).Methods("POST")
  router.HandleFunc("/api/eventowner", controllers.GetEventOwnerFor).Methods("GET")
  port := os.Getenv("PORT")
  if port == ""{
    port = "8000"
  }

  fmt.Println(port)

  err := http.ListenAndServe(":" + port, router)
  if err != nil{
    fmt.Print(err)
  }
}
