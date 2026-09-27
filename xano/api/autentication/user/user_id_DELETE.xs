// Delete user record.
query "user/{user_id}" verb=DELETE {
  api_group = "Autentication"

  input {
    int user_id? filters=min:1
  }

  stack {
    db.del user {
      field_name = "id"
      field_value = $input.user_id
    }
  }

  response = null
  guid = "JB_zNlJQ_g0Joff6jQdebwRLb-w"
}