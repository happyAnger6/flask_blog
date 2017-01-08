from flask import Flask
from webapp.config import DevConfig

app = Flask(__name__)
app.config.from_object(DevConfig)

if __name__ == '__main__':
    app.run(host='192.168.17.129')