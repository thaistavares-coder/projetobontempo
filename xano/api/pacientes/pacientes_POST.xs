// Create patient record
query pacientes verb=POST {
  api_group = "Pacientes"

  input {
    text nome filters=trim
    text telefone? filters=trim
    email email? filters=trim
  }

  stack {
    precondition ($input.nome != "") {
      error_type = "inputerror"
      error = "Nome é obrigatório."
    }

    function.run "validar_telefone_paciente" {
      input = {telefone: $input.telefone}
    } as $telefone_validado

    db.add paciente {
      data = {
        nome: $input.nome
        telefone: $input.telefone
        email: $input.email
      }
    } as $paciente
  }

  response = {
    id: $paciente.id
    nome: $paciente.nome
    telefone: $paciente.telefone
    email: $paciente.email
  }
  guid = "LHcbl0GvjpoQY7J4gnvWspZ_FEY"
}