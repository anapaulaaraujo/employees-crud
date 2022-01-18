from tornado.web import Application, RequestHandler
from tornado.ioloop import IOLoop
from database import connect_db
import json
from datetime import datetime
from authentication import create_password_hashed, create_token
import bcrypt
import jwt
from jwt.exceptions import ExpiredSignatureError


class EmployeesHandler(RequestHandler):
#Create a nutemployee entily with this payload
  def post(self):

    token = self.request.headers['token']
    header_data = jwt.get_unverified_header(token)
   
    #Verificando se o token não é nulo
    try:
      token
    except:
      self.set_status(400)
      self.write({'message':'Token Invalido'})
      return None

    #validando se o token esta expirado
    try:
      payload = jwt.decode(token, 'secret', 
      algorithms=[header_data['alg']])
    except jwt.ExpiredSignatureError as error:
      self.set_status(400)
      self.write(f'Token Expirado, error: {error}')
      return None

    db = connect_db()      
    req = json.loads(self.request.body)

     #Payload data error handling
    try:
      name = req["name"]
      birth_date = req["birth_date"]
      gender = req["gender"]
      email = req["email"]
      cpf = req["cpf"]
      start_date = req["start_date"]
      team = req["team"]
    except:
      self.set_status(400)
      self.write({'message':'Invalid Data'})
      return None

  #Validando formato de birth_date
    try:
      birth_date = datetime.strptime(birth_date, '%d/%m/%Y').strftime('%d/%m/%Y')
    except:
      self.set_status(400)
      self.write('This is the incorrect date string format. It should be DD/MM/YYYY')
      return None

  #Validando formato de start date
    try:
      start_date = datetime.strptime(start_date, '%m/%Y').strftime('%m/%Y')
    except:
      self.set_status(400)
      self.write('This is the incorrect date string format. It should be MM/YYYY')
      return None

  #Validando formato de cpf
    cpf = [int(char) for char in cpf if char.isdigit()]
    if len(cpf) != 11:
      self.set_status(400)
      self.write('CPF invalido')
      return None
      
    team_list = ['frontend', 'backend', 'fullstack', 'mobile']
    if team not in team_list:
      self.set_status(400)
      self.write('Please inform a valid team')
      return None

    gender_list = ['M','F', 'Other']
    if gender not in gender_list:
      self.set_status(400)
      self.write('Please inform a M, F or Other Gender')
      return None

    x = db.insert_one(req)

    self.write({ "msg": 'employee inserido com sucesso'})

#Get all nutemployee entities from the resource
  def get(self):

    try:
      self.request.headers['token']
    except:
      self.set_status(400)
      self.write({'message':'Token Invalido'})
      return None

    db = connect_db()
    employees = []
    
    for x in db.find({},{ "_id": 0}): 
        employees.append(x)

    self.write({'employees': employees})


class EmployeeHandler(RequestHandler):
  #Get a single nutemployee entily
    
  def get(self, payload):

    try:
      self.request.headers['token']
    except:
      self.set_status(400)
      self.write({'message':'Token Invalido'})
      return None

    print(payload)

    db = connect_db()
    query = {'name': payload}

    x = db.find_one(query, { "_id": 0})
        
    self.write({'response': x})

  #Update a nutemployee entily with this payload
  def put(self, payload):

    try:
      self.request.headers['token']
    except:
      self.set_status(400)
      self.write({'message':'Token Invalido'})
      return None

    db = connect_db()
    req = json.loads(self.request.body)

    query = {'name':payload}

    x = db.update_one(query, {"$set": req})
    
    self.write({ "msg": f'update'})

  #Delete a nutemployee entily
  def delete(self, payload):

    try:
      self.request.headers['token']
    except:
      self.set_status(400)
      self.write({'message':'Token Invalido'})
      return None

    db = connect_db()
    myquery = {'name':payload}

    x = db.delete_one(myquery)
    
    self.write({'response': 'employee deletado'})


class SignAuthHandler(RequestHandler):
  def post(self):

    req = json.loads(self.request.body)

    email = req["email"]
    password = req["senha"]

    password = create_password_hashed(password)
    
    #conetando e criando uma nova colletion no banco de dados
    db = connect_db(collection='usuarios')
    x = db.insert_one({'email': email, 'password': password})

    # precisa de uma f' para converter o password(bytes) em string
    self.write({ 'message': f'usuario cadastrado, email: {email}, password: {password}'})

class LoginAuthHandler(RequestHandler):

  def post(self):

    req = json.loads(self.request.body)
    email = req["email"]
    password = req["senha"]

    db = connect_db(collection='usuarios')

    #Consultando o db pelo email
    query = {'email': email}
 
    #Salvando o email e senha em user
    user = db.find_one(query, { "_id": 0})
    
    #se nao tiver conteudo em user, ou seja, nao encontrou o email, retorna none
    if not user:
      self.set_status(400)
      self.write({'response': 'email não cadastrado'}) 
      return None
    
    password = password.encode('utf-8')
    
     #comparando o password do body com o do banco
    if not bcrypt.checkpw(password, user['password']):
      self.set_status(400)
      self.write({'response': 'senha incorreta'}) 
      return None

    token = create_token(user)
    
    self.write({'token': token}) 

#endpoints
def make_app():
  urls = [("/nutemployee", EmployeesHandler), 
        (r"/nutemployee/?(.*)?", EmployeeHandler),
        ("/signauth", SignAuthHandler),
        ("/loginauth", LoginAuthHandler)]

  return Application(urls)


if __name__ == '__main__':
    app = make_app() 
    app.listen(8002) 
    IOLoop.instance().start() 