// Delete patient record
query "paciente/{paciente_id}" verb=DELETE {
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

    db.del paciente {
      field_name = "id"
      field_value = $input.paciente_id
    }
  }

  response = {success: true}
}