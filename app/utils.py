import pwd
from passlib.context import CryptContext

pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")

def hash(pwd:str):
   return pwd_context.hash(pwd)

def verify(text_pwd:str,hashed_pwd:str):
    return pwd_context.verify(text_pwd,hashed_pwd)