import hashlib

from cryptography.fernet import Fernet

from config import CRYPT_KEY

crypter = Fernet(CRYPT_KEY)


def get_hash_of_password(password):
  return hashlib.md5(password.encode("utf-8")).hexdigest()
