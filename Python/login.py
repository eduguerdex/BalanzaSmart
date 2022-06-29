import random
import pyrebase
config = {
  "apiKey": "Hi3wqSGBS8D4UJlLxJgAbudQHIEznTuUTe9famth",
  "authDomain": "proyectobalanzasmart.firebaseapp.com",
  "databaseURL": "https://proyectobalanzasmart-default-rtdb.firebaseio.com",
  "projectId": "proyectobalanzasmart",
  "storageBucket": "proyectobalanzasmart.appspot.com",
  "messagingSenderId": "893862381713",
  "appId": "1:893862381713:web:8ed11c18556d094e475730",
}

firebase = pyrebase.initialize_app(config)
storage=firebase.storage()
db = firebase.database()
# put the name of your database where the ***** are
print("Send Data to Firebase Using Raspberry Pi")
a=random.randrange(20)/2.5
print(a)
UDNI=70088669


datosDNI = {'DNI':UDNI}
lista_data=["Manzana","Banana"]
letras = {'Productos':lista_data}

db.child("Cliente").update(datosDNI)
db.child("Cliente").update(letras)
print("Data agregada")
