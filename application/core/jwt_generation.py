from jose import jwt

from application.core.config import settings


class JWTGeneration:
    #Doc String

    @classmethod
    def encode_jwt(
        cls,
        *,
        payload: dict,
        private_key: str = settings.jwt_settings.private_key_path.read_text(),
        algorithm: str = settings.jwt_settings.algorithm
    ) -> str:
        #Doc String

        return jwt.encode(payload, key=private_key, algorithm=algorithm)
    

    @classmethod
    def decode_jwt(
        cls, 
        *, 
        access_token: str | bytes,
        public_key: str = settings.jwt_settings.public_key_path.read_text(),
        algorithm: str = settings.jwt_settings.algorithm
    ) -> str:
        #Doc String

        return jwt.decode(access_token=access_token, key=public_key, algorithms=[algorithm], options={"verify_exp": True})