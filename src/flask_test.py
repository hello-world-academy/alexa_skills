from flask import Flask
app = Flask(__name__)
@app.route('/')
def homepage():
    return "Welcome to the Hacker News Reader, an Alexa app to get the top trending stories in the digital sphere."

if __name__ == '__main__':
    app.run(debug=True)