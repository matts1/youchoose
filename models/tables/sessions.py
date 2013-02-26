from functions.db import *
from string import *
import random

def create(email):
    id = "".join([random.choice(ascii_letters + digits) for i in range(200)])
    query("INSERT INTO sessions VALUES (?, ?, datetime('now', '+1 day'))", [id, email])
    return id

def delete(id):
    query("DELETE FROM sessions WHERE id=?", [id])

def get(id):
    query("DELETE FROM sessions WHERE expiry < datetime('now')")
    query("UPDATE sessions set expiry=datetime('now', '+1 day') WHERE id=?", [id])
    email = queryone("SELECT email FROM sessions WHERE id=?", [id])
    return None if email is None else email[0]