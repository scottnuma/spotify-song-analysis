from flask import Flask
from flask import render_template
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'hello'

@app.route('/static/<path:path>')
def sender(path):
    return send_from_directory('static', path)

if __name__ == "__main__":
    app.run(port=8000)
