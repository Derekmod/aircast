from dataclasses import dataclass


@dataclass
class Question:
    question: str
    correct_answer: str
    other_answers: list[str]


@dataclass
class Module:
    name: str
    blurb: str
    questions: list[Question]


@dataclass
class PaperCurriculum:
    overview_module: Module
    # content_modules: list[Module]
    # conclusion_module: Module
