from dataclasses import dataclass
from pdfminer.high_level import extract_text
import requests
import tempfile


@dataclass
class PaperSection:
    header: str
    content: str
    # figures


@dataclass
class ParsedPaper:
    sections: list[PaperSection]


def parse_pdf(filename: str):
    return extract_text(filename)


def parse_content_with_headings(text: str) -> list[PaperSection]:
    lines = text.split("\n")
    sections: list[PaperSection] = []
    current_heading = None
    current_content = ""

    for line in lines:
        # This condition checks if the line is in uppercase and has content (not just whitespace)
        if line.isupper() and line.strip():
            if current_heading:
                sections.append({"header": current_heading, "content": current_content.strip()})
                current_content = ""  # Reset current_content for the next section
            current_heading = line.strip()
        elif current_heading:
            current_content += line + "\n"

    # To handle the content under the last heading
    if current_heading and current_content:
        sections.append(
            PaperSection(
                header=current_heading,
                content=current_content.strip(),
            )
        )

    return sections


def download_pdf(url: str) -> str:
    response = requests.get(url)

    if response.status_code == 200:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tfile:
            tfile.write(response.content)
            return tfile.name
    else:
        raise ValueError(f"Failed to download PDF. Status code: {response.status_code}")


def parse_url(url: str) -> ParsedPaper:
    pdf_file = download_pdf(url)
    if pdf_file:
        text = parse_pdf(pdf_file)
        parsed_content = parse_content_with_headings(text)

    return ParsedPaper(
        sections=parsed_content,
    )
