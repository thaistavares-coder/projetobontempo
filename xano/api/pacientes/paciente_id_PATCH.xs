// Edit patient record
query "paciente/{paciente_id}" verb=PATCH {
  api_group = "Pacientes"

  input {
    int paciente_id filters=min:1
    text nome? filters=trim
    text telefone? filters=trim
    email email? filters=trim
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

    precondition (($input.nome == null) || ($input.nome != "")) {
      error_type = "inputerror"
      error = "Nome não pode estar vazio."
    }

    function.run "validar_telefone_paciente" {
      input = {telefone: $input.telefone}
    } as $telefone_validado

    db.patch paciente {
      field_name = "id"
      field_value = $input.paciente_id
      data = {nome: $input.nome, telefone: $input.telefone, email: $input.email}|filter_null
    } as $paciente_atualizado
  }

  response = {
    id: $paciente_atualizado.id
    nome: $paciente_atualizado.nome
    telefone: $paciente_atualizado.telefone
    email: $paciente_atualizado.email
  }
  guid = "QG6BC-WKWdO5UYLAkmmWZO-1ncg"
}