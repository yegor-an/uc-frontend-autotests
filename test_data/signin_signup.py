# Валидационные данные
INVALID_EMAIL_ONLY_LETTERS = "abcdef"
INVALID_EMAIL_NO_AT = "userdomain.com"
INVALID_EMAIL_NO_DOT = "user@domain"
INVALID_EMAIL_WITH_SPACES = "  user@mail.com  "
INVALID_EMAIL_DOUBLE_AT = "user@@mail.com"
INVALID_EMAIL_DOUBLE_DOT = "a..b@mail.com"
VALID_EMAIL = 'la@la.la'

INVALID_PASSWORD_SHORT = 'la'
INVALID_PASSWORD_LONG = 'l' * 65
VALID_PASSWORD = 'lalalala'

UNEXISTING_EMAIL = 'allo@yopta.etoty'
UNMATCHING_PASSWORD = 'harry_potter'

# Сообщения об ошибках
ERROR_EMAIL_INVALID = 'Email not valid'
ERROR_PASSWORD_MIN = 'Min. 8 characters'
ERROR_PASSWORD_MAX = 'Max. 64 characters'
ERROR_TAKEN_EMAIL = 'Email already taken'
