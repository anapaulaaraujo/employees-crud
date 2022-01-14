from tornado.web import Application, RequestHandler
from tornado.ioloop import IOLoop
from database import connect_db
import json

class EmployeesHandler(RequestHandler):
#Create a nutemployee entily with this payload
  def post(self):
    db = connect_db()      
    req = json.loads(self.request.body)
    x = db.insert_one(req)

    self.write({ "msg": 'employee inserido com sucesso'})

#Get all nutemployee entities from the resource
  def get(self):

    db = connect_db()
    employees = []
    
    for x in db.find({},{ "_id": 0}): 
        employees.append(x)

    self.write({'employees': employees})


class EmployeeHandler(RequestHandler):
  #Get a single nutemployee entily
  def get(self, payload):
    print(payload)

    db = connect_db()
    query = {'name': payload}

    x = db.find_one(query, { "_id": 0})
        
    self.write({'response': x})

  #Update a nutemployee entily with this payload
  def put(self, payload):

    db = connect_db()
    req = json.loads(self.request.body)

    query = {'name':payload}

    x = db.update_one(query, {"$set": req})
    
    self.write({ "msg": f'update'})

  #Delete a nutemployee entily
  def delete(self, payload):

    db = connect_db()
    myquery = {'name':payload}

    x = db.delete_one(myquery)

    self.write({'response': 'employee deletado'})


#endpoints
def make_app():
  urls = [("/nutemployee", EmployeesHandler), 
        (r"/nutemployee/?(.*)?", EmployeeHandler)]

  return Application(urls)


if __name__ == '__main__':
    app = make_app() 
    app.listen(8002) 
    IOLoop.instance().start() 