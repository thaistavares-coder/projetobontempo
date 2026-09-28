// Get patient record
query "paciente/{paciente_id}" verb=GET {
  api_group = "Pacientes"

  input {
    int paciente_id filters=min:1
  }

  stack {
    db.get paciente {
      field_name = "id"
      field_value = $input.paciente_id
    } as $paciente

    precondition ($paciente != null) {
      error_type = "notfound"
      error = "Paciente não encontrado."
    }
  }

  response = {
    id: $paciente.id
    nome: $paciente.nome
    telefone: $paciente.telefone
    email: $paciente.email
  }
  guid = "lSK6195ZUGVuCcZFf-AFIuZMoWY"
}