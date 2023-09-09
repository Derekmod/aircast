from flask import Flask, request

from backend.paper_parsing import parse_url
from utils.path_utils import PROJECT_ROOT_PATH

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

        parsed_content = parse_url(url)

        if parsed_content:
            try:
                paper_contents_dir = PROJECT_ROOT_PATH / "paper_contents"
                paper_contents_dir.mkdir(exist_ok=True)

                with open(f"paper_contents/{url}", "w") as file:
                    file.write(parsed_content)
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
