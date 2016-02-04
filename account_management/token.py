from itsdangerous import URLSafeTimedSerializer
from config import BaseConfig


class Token():

    def generate_confirmation_token(self, email):
        serializer = URLSafeTimedSerializer(BaseConfig.SECRET_KEY)
        return serializer.dumps(email, salt=BaseConfig.SECURITY_PASSWORD_SALT)

    def confirm_token(self, token, expiration=3600):
        serializer = URLSafeTimedSerializer(BaseConfig.SECRET_KEY)
        try:
            email = serializer.loads(
                token,
                salt=BaseConfig.SECURITY_PASSWORD_SALT,
                max_age=expiration
            )
        except:
            return False
        return email

def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(BaseConfig.SECRET_KEY)
    try:
        email = serializer.loads(
            token,
            salt=BaseConfig.SECURITY_PASSWORD_SALT,
            max_age=expiration
        )
    except:
        return False
    return email
