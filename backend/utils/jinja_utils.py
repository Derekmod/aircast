from pathlib import Path
from jinja2 import Template
from typing import Any


def load_template(path: Path) -> Template:
    with path.open("rt") as fin:
        return Template(fin.read())


def get_render_args(args: dict[str, Any]) -> dict[str, Any]:
    """Usage: template.render(**get_render_args(locals()))"""
    if "self" in args:
        assert "this" not in args
        args["this"] = args["self"]
        del args["self"]

    return args
