import bcrypt
import base64

class AuthHelper:
  def __init__(self): pass

  def encode_password(self, password: str) -> bytes:
    return password.encode('utf-8')

  def hash_password(self, password: str) -> bytes:
    hashedPassword = base64.b64encode(bcrypt.hashpw(self.encode_password(password), bcrypt.gensalt(10)))
    return hashedPassword

  def is_password_match(self, password: str, b64_password: bytes) -> bool:
    '''`b64_password` parameter is from DB wich has been encoded in base64'''
    decoded_hashed_password = base64.b64decode(b64_password)
    is_match = bcrypt.checkpw(self.encode_password(password), decoded_hashed_password)
    return is_match