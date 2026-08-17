import phonenumbers
from phonenumbers import NumberParseException, PhoneNumberFormat


class PhoneValidationError(ValueError):
    code = "INVALID_PHONE"


def normalize_ma_phone(raw: str) -> tuple[str, str]:
    value = (raw or "").strip()
    if not value:
        raise PhoneValidationError("رقم التيليفون مطلوب")

    try:
        parsed = phonenumbers.parse(value, "MA")
    except NumberParseException as exc:
        raise PhoneValidationError("رقم التيليفون المغربي غير صالح") from exc

    if not phonenumbers.is_valid_number(parsed):
        raise PhoneValidationError("رقم التيليفون المغربي غير صالح")

    region = phonenumbers.region_code_for_number(parsed)
    if region != "MA":
        raise PhoneValidationError("خص رقم مغربي (06 أو 07)")

    number_type = phonenumbers.number_type(parsed)
    if number_type not in (
        phonenumbers.PhoneNumberType.MOBILE,
        phonenumbers.PhoneNumberType.FIXED_LINE_OR_MOBILE,
    ):
        raise PhoneValidationError("رقم التيليفون المغربي غير صالح")

    e164 = phonenumbers.format_number(parsed, PhoneNumberFormat.E164)
    national = phonenumbers.format_number(parsed, PhoneNumberFormat.NATIONAL)
    display = national.replace(" ", "").replace("-", "")
    return e164, display


def normalize_ksa_phone(raw: str) -> tuple[str, str]:
    """Compatibility wrapper — Morocco store uses MA numbers."""
    return normalize_ma_phone(raw)
