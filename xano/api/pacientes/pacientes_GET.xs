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

  response = $pacientes|map:{
    id: $$.id
    nome: $$.nome
    telefone: $$.telefone
    email: $$.email
  }
  guid = "cqrGWH1c967VroPTOqLu-NiatkI"
}