import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

credential = credentials.ApplicationDefault()
firebase_admin.initialize_app(credential)

db = firestore.client()

def _get_all(collection):
  return db.collection(collection).get()

def get_users():
  return _get_all('users')

def get_todos(user_id):
  return db.collection('users').document(user_id).collection('todos').get()
