from itsdangerous import URLSafeTimedSerializer
from config import BaseConfig

class Token():

    @staticmethod
    def generate_confirmation_token(email):
        serializer = URLSafeTimedSerializer(BaseConfig.SECRET_KEY)
        return serializer.dumps(email, salt=BaseConfig.SECURITY_PASSWORD_SALT)

    @staticmethod
    def confirm_token(token, expiration=43200):
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