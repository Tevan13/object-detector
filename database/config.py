import firebase_admin
from firebase_admin import credentials, db

cred = credentials.Certificate("./firebase.json")
default_app = firebase_admin.initialize_app(cred, {
  'databaseURL': 'https://scan-18376-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

ref = db.reference('./data.json')

data_string = "Contoh string untuk disimpan"
ref.set(data_string)

print("String berhasil disimpan.")