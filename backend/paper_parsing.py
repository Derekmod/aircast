from dataclasses import dataclass


@dataclass
class PaperSection:
    header: str
    content: str
    # figures


@dataclass
class ParsedPaper:
    sections: list[PaperSection]


def parse_url(url: str) -> ParsedPaper:
    # TODO: stub
    return ParsedPaper(
        sections=[],
    )
