import phonenumbers
from phonenumbers import NumberParseException, PhoneNumberFormat


class PhoneValidationError(ValueError):
    code = "INVALID_PHONE"


def normalize_ksa_phone(raw: str) -> tuple[str, str]:
    """
    Validate and normalize a Saudi mobile number.
    Returns (e164, display) e.g. (+966501234567, 0501234567).
    """
    value = (raw or "").strip()
    if not value:
        raise PhoneValidationError("رقم الجوال مطلوب")

    try:
        parsed = phonenumbers.parse(value, "SA")
    except NumberParseException as exc:
        raise PhoneValidationError("رقم الجوال غير صالح") from exc

    if not phonenumbers.is_valid_number(parsed):
        raise PhoneValidationError("رقم الجوال غير صالح")

    region = phonenumbers.region_code_for_number(parsed)
    if region != "SA":
        raise PhoneValidationError("يجب أن يكون رقم سعودي")

    number_type = phonenumbers.number_type(parsed)
    if number_type not in (
        phonenumbers.PhoneNumberType.MOBILE,
        phonenumbers.PhoneNumberType.FIXED_LINE_OR_MOBILE,
    ):
        raise PhoneValidationError("رقم الجوال غير صالح")

    e164 = phonenumbers.format_number(parsed, PhoneNumberFormat.E164)
    national = phonenumbers.format_number(parsed, PhoneNumberFormat.NATIONAL)
    display = national.replace(" ", "").replace("-", "")
    return e164, display
