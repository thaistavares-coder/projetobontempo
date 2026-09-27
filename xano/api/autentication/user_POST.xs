// Add user record
query user verb=POST {
  api_group = "Autentication"

  input {
    dblink {
      table = "user"
    }
  }

  stack {
    db.add user {
      enforce_hidden_fields = false
      data = {created_at: "now"}
    } as $user
  }

  response = $user
  guid = "xqsIA0pYsGSHRN4lg82vPvLxYeI"
}