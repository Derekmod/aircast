from flask import Flask, request
from any_serde import to_data

from backend.paper_parsing import parse_url, ParsedPaper
from backend.curriculum import PaperCurriculum
from backend.curriculum_generation import generate_curriculum
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

        parsed_paper = parse_url(url)
        parsed_paper_data = to_data(ParsedPaper, parsed_paper)

        try:
            paper_contents_dir = PROJECT_ROOT_PATH / "paper_contents"
            paper_contents_dir.mkdir(exist_ok=True)

            with open(f"paper_contents/{url}", "w") as file:
                file.write(parsed_paper_data)
            return "Parsed paper saved successfully!"
        except Exception as e:
            raise ValueError("Error saving aper contents!") from e
    else:
        return "Invalid request method"


@app.route("/curriculum", methods=["POST"])
def get_curriculum():
    if request.method == "POST":
        url = request.form.get("data")
        if not isinstance(url, str):
            raise ValueError("Bad data type!")

        parsed_content = parse_url(url)

        curriculum = generate_curriculum(url, parsed_content)
        curriculum_data = to_data(PaperCurriculum, curriculum)
        return curriculum_data
    else:
        return "Invalid request method"


# Call with `PYTHONPATH=. python backend/app.py`
if __name__ == "__main__":
    app.run()
