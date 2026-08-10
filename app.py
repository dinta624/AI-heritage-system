from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello! Your Heritage AI project is working!"

if __name__ == '__main__':
    app.run(debug=True)