from backend.curriculum import PaperCurriculum, Question, Module
from backend.paper_parsing import ParsedPaper
from claude.generator import generate, Trajectory, Turn
import yaml
import any_serde
from utils.jinja_utils import load_template, get_render_args
import copy
from pathlib import Path
import re

from utils.path_utils import PROJECT_ROOT_PATH


MESSAGES_DIR = PROJECT_ROOT_PATH / "backend" / "messages"
GENERATION_RESULTS_DIR = PROJECT_ROOT_PATH / "generations"


_UNIQUE_IDX = 0


def get_unique_idx() -> int:
    global _UNIQUE_IDX
    _UNIQUE_IDX += 1
    return _UNIQUE_IDX


def get_blurb(paper_results_dir: Path, parsed_content: ParsedPaper) -> tuple[Trajectory, str]:
    with (MESSAGES_DIR / "initial_trajectory.yaml").open("rt") as fin_traj:
        traj_data = yaml.load(fin_traj, Loader=yaml.SafeLoader)

    traj = any_serde.from_data(Trajectory, traj_data)

    prompt_template = load_template(MESSAGES_DIR / "blurb_prompt.jinja2")
    prompt = prompt_template.render(**get_render_args(locals()))
    traj.turns.append(
        Turn(
            user_message=prompt,
            assistant_message=None,
        ),
    )
    response = generate(traj, save_path=paper_results_dir / "blurb.yaml")
    traj.turns[-1].assistant_message = response

    raw_blurb_traj = copy.deepcopy(traj)

    redo_prompt_template = load_template(MESSAGES_DIR / "blurb_redo_prompt.jinja2")
    redo_prompt = redo_prompt_template.render(**get_render_args(locals()))
    traj.turns.append(
        Turn(
            user_message=redo_prompt,
            assistant_message=None,
        ),
    )
    redo_response = generate(traj, save_path=paper_results_dir / "blurb_redo.yaml")

    return raw_blurb_traj, redo_response


def get_question_answers(
    paper_results_dir: Path,
    traj: Trajectory,
    question_line: str,
    question_idx: int,
    question: str,
) -> tuple[str, list[str]]:
    answers_template = load_template(MESSAGES_DIR / "get_answers.jinja2")
    answers_prompt = answers_template.render(**get_render_args(locals()))
    traj.turns.append(
        Turn(
            user_message=answers_prompt,
            assistant_message=None,
        ),
    )
    response = generate(traj, save_path=paper_results_dir / f"answers_{get_unique_idx()}.yaml")

    answers: list[str] = []
    for answer_line in response.split("\n"):
        answer_line = answer_line.strip()
        if not answer_line:
            continue

        answer_match = re.fullmatch(r"(?:\d+[\.:\)] )?(.*)", answer_line)
        assert answer_match
        answers.append(answer_match.group(1))

    return answers[0], answers[1:]


def reformat_response_as_questions(paper_results_dir: Path, traj: Trajectory) -> list[Question]:
    reformat_questions_template = load_template(MESSAGES_DIR / "reformat_questions.jinja2")
    reformat_questions_prompt = reformat_questions_template.render(**get_render_args(locals()))
    traj.turns.append(
        Turn(
            user_message=reformat_questions_prompt,
            assistant_message=None,
        ),
    )
    response = generate(traj, save_path=paper_results_dir / "reformat_response_as_question.yaml")
    traj.turns[-1].assistant_message = response
    question_lines = response.split("\n")

    questions: list[Question] = []
    for question_line in question_lines:
        question_line = question_line.strip()
        if not question_line:
            continue
        match = re.fullmatch(r"(\d+)\. (.*)", question_line)
        assert match
        question_idx = int(match.group(1))
        question = match.group(2)
        correct_answer, incorrect_answers = get_question_answers(
            paper_results_dir,
            copy.deepcopy(traj),
            question_line,
            question_idx,
            question,
        )
        questions.append(Question(question=question, correct_answer=correct_answer, other_answers=incorrect_answers))

    return questions


def generate_questions_from_blurb_traj(paper_results_dir: Path, traj: Trajectory) -> list[Question]:
    question_prompt_template = load_template(MESSAGES_DIR / "questions_from_blurb.jinja2")
    question_prompt = question_prompt_template.render(**get_render_args(locals()))
    traj.turns.append(
        Turn(
            user_message=question_prompt,
            assistant_message=None,
        ),
    )
    response = generate(traj, save_path=paper_results_dir / f"questions_from_blurb_{get_unique_idx()}.yaml")
    traj.turns[-1].assistant_message = response

    return reformat_response_as_questions(paper_results_dir, copy.deepcopy(traj))


def generate_curriculum(url: str, parsed_content: ParsedPaper) -> PaperCurriculum:
    paper_results_dir = GENERATION_RESULTS_DIR / url.replace("/", "")
    paper_results_dir.mkdir(parents=True, exist_ok=True)
    raw_blurb_traj, blurb = get_blurb(paper_results_dir, parsed_content)
    questions = generate_questions_from_blurb_traj(paper_results_dir, raw_blurb_traj)

    return PaperCurriculum(
        overview_module=Module(
            name="overview",
            # blurb="The paper is about things and things are cool.",
            blurb=blurb,
            questions=questions,
        ),
    )
