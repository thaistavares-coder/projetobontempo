import re


_EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def validate_contact(name: str, phone: str, email: str) -> str | None:
    if not name.strip():
        return "Informe o nome."
    if not phone.strip():
        return "Informe o telefone."
    if email.strip() and not _EMAIL_PATTERN.fullmatch(email.strip()):
        return "Informe um email válido ou deixe o campo vazio."
    return None
