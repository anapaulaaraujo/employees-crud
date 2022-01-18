import bcrypt
import jwt

def create_password_hashed(password):
    #encoding para colocar o b'
    password = password.encode('utf-8')
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())

    return hashed

def create_token(user):

    user['password'] = user['password'].decode('utf-8')

    token = jwt.encode(user, "secret", algorithm="HS256")

    return token