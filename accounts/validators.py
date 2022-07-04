from django.core.exceptions import ValidationError

def validate_symbols(value):
    if (not value.endswith('dongguk.edu')) or (not value.endswith('dgu.edu')):
        raise ValidationError("동국대학교 이메일로만 가입이 가능합니다.", code='symbol-err')