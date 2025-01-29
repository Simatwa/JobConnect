import uuid
import hashlib
import secrets
import random
from string import ascii_lowercase


def generate_uuid4_token():
    return str(uuid.uuid4())


def generate_token():
    return "jbc_" + str(uuid.uuid4()).replace("-", random.choice(ascii_lowercase))


# Usage
a = generate_token()

print(a)

# Store hashed_uuid4_token securely
