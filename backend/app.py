from flask import Flask, request

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<html><head><title>Hello World</title></head><body><h1>Hello, World!</h1></body></html>"


@app.route("/parse_paper", methods=["POST"])
def save_paper_contents():
    if request.method == "POST":
        url = request.form.get("data")
        if not isinstance(url, str):
            raise ValueError("Bad data type!")

        if url:
            try:
                with open(f"paper_contents/{url}", "w") as file:
                    file.write(url)
                return "String saved successfully!"
            except Exception as e:
                raise ValueError("Error saving string!") from e
        else:
            return "No url received!"
    else:
        return "Invalid request method"


# Call with `python backend/app.py`
if __name__ == "__main__":
    app.run()
