from dataclasses import dataclass


@dataclass
class Question:
    question: str
    correct_answer: str
    other_answers: list[str]


@dataclass
class Content:
    message: str
    questions: list[Question]


@dataclass
class Module:
    name: str
    content: list[Content]


@dataclass
class Curriculum:
    overview_module: Module
    content_modules: list[Module]
    conclusion_module: Module