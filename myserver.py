from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Server is runing"
def run():
    app.run(host='0.0.0.0',port=8080)
    
degf server_on(0)