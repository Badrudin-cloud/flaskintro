from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return "<h1>Hello world</h1>"


@app.route('/home')
def home():
    return render_template('index.html')


if __name__ == "__main__":
    app.run()