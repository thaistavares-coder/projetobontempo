// List patient records
query pacientes verb=GET {
  api_group = "Pacientes"

  input {
  }

  stack {
    db.query paciente {
      return = {type: "list"}
    } as $pacientes
  }

  response = $pacientes
}