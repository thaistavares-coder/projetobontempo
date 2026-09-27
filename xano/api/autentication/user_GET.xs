// Query all user records
query user verb=GET {
  api_group = "Autentication"

  input {
  }

  stack {
    db.query user {
      return = {type: "list"}
    } as $user
  }

  response = $user
  guid = "uuJ1c4jcV_RLYpPz64R9BOw4wcI"
}