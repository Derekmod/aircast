from backend.curriculum import PaperCurriculum, Question, Module
from backend.paper_parsing import ParsedPaper


def generate_curriculum(parsed_content: ParsedPaper) -> PaperCurriculum:
    del parsed_content
    return PaperCurriculum(
        overview_module=Module(
            name="overview",
            blurb="The paper is about things and things are cool.",
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
