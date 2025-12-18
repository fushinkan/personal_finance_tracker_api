import bcrypt

class Password:
    #Doc String

    @classmethod
    def hashed_psw(
        cls, 
        *, 
        password: str
    ) -> str:
        #Doc String

        return bcrypt.hashpw(password=password.encode("utf-8"), salt=bcrypt.gensalt()).decode("utf-8")
    

    @classmethod
    def verify_password(
        cls, 
        *, 
        plain_password: str,
        hashed_password: str
    ) -> bool:
        #Doc String

        return bcrypt.checkpw(password=plain_password.encode("utf-8"), hashed_password=hashed_password.encode("utf-8"))