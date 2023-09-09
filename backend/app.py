from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<html><head><title>Hello World</title></head><body><h1>Hello, World!</h1></body></html>"


if __name__ == "__main__":
    app.run()
