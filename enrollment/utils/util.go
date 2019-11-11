package utils

import (
  "encoding/json"
  "net/http"
  "crypto/sha1"
  "encoding/hex"
)

func Message(status bool, message string) (map[string]interface{}){
  return map[string]interface{} {"status": status, "message": message}
}

func Respond(w http.ResponseWriter, data map[string] interface{}){
  w.Header().Add("Content-Type", "application/json")
  json.NewEncoder(w).Encode(data)
}

func Hash(s string)(string){
  h := sha1.New()
  h.Write([]byte(s))
  bs := hex.EncodeToString(h.Sum(nil))
  return bs
}
