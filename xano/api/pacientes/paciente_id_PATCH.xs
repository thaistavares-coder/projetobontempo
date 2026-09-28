// Edit patient record
query "paciente/{paciente_id}" verb=PATCH {
  api_group = "Pacientes"

  input {
    int paciente_id filters=min:1
    text nome?="__xano_missing_nome_4bd7f28f__"
    text telefone?="__xano_missing_telefone_4bd7f28f__"
    email email?="missing-paciente-field-4bd7f28f@invalid.invalid"
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

    precondition (($input.nome == "__xano_missing_nome_4bd7f28f__") || (($input.nome != null) && (($input.nome|trim) != ""))) {
      error_type = "inputerror"
      error = "Nome não pode estar vazio."
    }

    conditional {
      if ($input.telefone != "__xano_missing_telefone_4bd7f28f__") {
        function.run "validar_telefone_paciente" {
          input = {telefone: $input.telefone}
        } as $telefone_validado
      }
    }

    var $updates {
      value = {}
    }

    conditional {
      if ($input.nome != "__xano_missing_nome_4bd7f28f__") {
        var.update $updates.nome {
          value = $input.nome|trim
        }
      }
    }

    conditional {
      if (($input.telefone != "__xano_missing_telefone_4bd7f28f__") && (($input.telefone == null) || ($input.telefone == ""))) {
        var.update $updates.telefone {
          value = null
        }
      }
    }

    conditional {
      if (($input.telefone != "__xano_missing_telefone_4bd7f28f__") && ($input.telefone != null) && ($input.telefone != "")) {
        var.update $updates.telefone {
          value = $input.telefone
        }
      }
    }

    conditional {
      if (($input.email != "missing-paciente-field-4bd7f28f@invalid.invalid") && (($input.email == null) || ($input.email == ""))) {
        var.update $updates.email {
          value = null
        }
      }
    }

    conditional {
      if (($input.email != "missing-paciente-field-4bd7f28f@invalid.invalid") && ($input.email != null) && ($input.email != "")) {
        var.update $updates.email {
          value = $input.email
        }
      }
    }

    var $paciente_atualizado {
      value = $paciente
    }

    conditional {
      if (($updates|is_empty) == false) {
        db.patch paciente {
          field_name = "id"
          field_value = $input.paciente_id
          data = $updates
        } as $resultado_patch

        var.update $paciente_atualizado {
          value = $resultado_patch
        }
      }
    }
  }

  response = {
    id: $paciente_atualizado.id
    nome: $paciente_atualizado.nome
    telefone: $paciente_atualizado.telefone
    email: $paciente_atualizado.email
  }
  guid = "QG6BC-WKWdO5UYLAkmmWZO-1ncg"
}