function "validar_telefone_paciente" {
  description = "Valida o formato básico do telefone de um paciente"

  input {
    text telefone?
  }

  stack {
    var $phone {
      value = $input.telefone|first_notnull:""
    }

    var $format_valido {
      value = "/^[+]?[0-9 ()-]+$/"|regex_matches:$phone
    }

    var $digits {
      value = $phone|replace:" ":""|replace:"(":""|replace:")":""|replace:"-":""|replace:"+":""
    }

    precondition (($input.telefone == null) || ($input.telefone == "") || ($format_valido && (($digits|strlen) >= 8) && (($digits|strlen) <= 15))) {
      error_type = "inputerror"
      error = "Telefone inválido."
    }
  }

  response = true
  guid = "15bPr2s8GFSEqHJHMHK11mImCpI"
}