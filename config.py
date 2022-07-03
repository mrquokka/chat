import os

CRYPT_KEY = (
  os.environ.get("CRYPT_KEY", None)
  or "9gYclSnEp-BJIk--kARyHOYUbHmjZDa69oOnBX9fK8w="
)
NAMESPACE = "/socket"


STATIC_DIR = os.environ.get("STATIC_DIR", None) or os.path.join(
  os.path.dirname(__file__), "static"
)
