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
    raw_text: str
    sections: list[PaperSection]

    def get_abstract(self) -> str:
        raise NotImplementedError()

    def get_introduction(self) -> str:
        raise NotImplementedError()

    def get_conclusion(self) -> str:
        raise NotImplementedError()


def parse_pdf(filename: str):
    return extract_text(filename)


def parse_content_with_headings(text: str) -> ParsedPaper:
    lines = text.split("\n")
    sections: list[PaperSection] = []
    current_heading = None
    current_content = ""

    for line in lines:
        # This condition checks if the line is in uppercase and has content (not just whitespace)
        if line.isupper() and line.strip():
            if current_heading:
                sections.append(
                    PaperSection(
                        header=current_heading,
                        content=current_content.strip(),
                    ),
                )
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
            ),
        )

    return ParsedPaper(
        raw_text=text,
        sections=sections,
    )


def download_pdf(url: str) -> str:
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
            " AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.1000.0 Safari/537.36"
        ),
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        # Add any other headers you want to include
    }
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
            " AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        ),
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tfile:
            tfile.write(response.content)
            return tfile.name
    else:
        raise ValueError(f"Failed to download PDF. Status code: {response.status_code}")


def parse_url(url: str) -> ParsedPaper:
    pdf_file = download_pdf(url)
    assert pdf_file

    text = parse_pdf(pdf_file)
    return parse_content_with_headings(text)
