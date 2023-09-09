from backend.curriculum import PaperCurriculum, Question, Module
from backend.paper_parsing import ParsedPaper
from claude.generator import generate, Trajectory, Turn
import yaml
import any_serde
from utils.jinja_utils import load_template, get_render_args

from utils.path_utils import PROJECT_ROOT_PATH


MESSAGES_DIR = PROJECT_ROOT_PATH / "backend" / "messages"
GENERATION_RESULTS_DIR = PROJECT_ROOT_PATH / "generations"


def get_blurb(url: str, parsed_content: ParsedPaper) -> str:
    paper_results_dir = GENERATION_RESULTS_DIR / url.replace("/", "")
    paper_results_dir.mkdir(parents=True, exist_ok=True)

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

    redo_prompt_template = load_template(MESSAGES_DIR / "blurb_redo_prompt.jinja2")
    redo_prompt = redo_prompt_template.render(**get_render_args(locals()))
    traj.turns.append(
        Turn(
            user_message=redo_prompt,
            assistant_message=None,
        ),
    )
    redo_response = generate(traj, save_path=paper_results_dir / "blurb_redo.yaml")

    return redo_response


def generate_curriculum(url: str, parsed_content: ParsedPaper) -> PaperCurriculum:
    blurb = get_blurb(url, parsed_content)

    return PaperCurriculum(
        overview_module=Module(
            name="overview",
            # blurb="The paper is about things and things are cool.",
            blurb=blurb,
            questions=[
                Question(
                    question="Why is the paper cool?",
                    correct_answer="Things are cool.",
                    other_answers=[
                        "Objects are rad.",
                        "I am a turtle",
                    ],
                ),
                Question(
                    question="What is the paper about?",
                    correct_answer="things",
                    other_answers=[
                        "Stuff",
                        "Junk",
                        "Something",
                    ],
                ),
            ],
        ),
    )
