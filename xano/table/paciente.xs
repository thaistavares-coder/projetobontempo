// paciente
table paciente {
  auth = false

  schema {
    int id
    text nome filters=trim
    text telefone?
    email email? filters=trim
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
  ]
}