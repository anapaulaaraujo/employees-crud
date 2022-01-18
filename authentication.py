import bcrypt
import jwt
import datetime


def create_password_hashed(password):
    #encoding para colocar o b'
    password = password.encode('utf-8')
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())

    return hashed

def create_token(user):

    user['password'] = user['password'].decode('utf-8')
    user['exp'] = datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(seconds=30)

    token = jwt.encode(user, "secret", algorithm="HS256")

    return token