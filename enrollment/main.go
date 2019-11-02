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
