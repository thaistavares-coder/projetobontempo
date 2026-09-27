// user
table user {
  auth = false

  schema {
    int id
    timestamp created_at?=now {
      visibility = "private"
    }
  
    text name? filters=trim
    email email? filters=trim|lower
    password password? {
      sensitive = true
      visibility = "internal"
    }
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "created_at", op: "desc"}]}
  ]

  guid = "kl9rAKtfnDA-n9WGisvITmvk1LE"
}