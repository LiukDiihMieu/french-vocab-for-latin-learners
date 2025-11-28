#!/usr/bin/env python3
import pathlib

import yaml
from jinja2 import Environment, FileSystemLoader


ROOT = pathlib.Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
TEMPLATE_DIR = ROOT / "templates"
OUTPUT_DIR = ROOT / "build"
OUTPUT_MD = OUTPUT_DIR / "vocab.md"


def load_yaml(path: pathlib.Path):
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    # Sort by index just to be sure
    return sorted(data, key=lambda e: e["index"])


def main() -> None:
    nouns_path = DATA_DIR / "nouns.yaml"
    adjectives_path = DATA_DIR / "adjectives.yaml"
    verbs_path = DATA_DIR / "verbs.yaml"

    nouns = load_yaml(nouns_path)
    adjectives = load_yaml(adjectives_path)
    verbs = load_yaml(verbs_path)

    env = Environment(
        loader=FileSystemLoader(str(TEMPLATE_DIR)),
        autoescape=False,
        trim_blocks=True,
        lstrip_blocks=True,
    )
    template = env.get_template("vocab.md.j2")

    rendered = template.render(nouns=nouns, adjectives=adjectives, verbs=verbs)

    OUTPUT_DIR.mkdir(exist_ok=True)
    with OUTPUT_MD.open("w", encoding="utf-8") as f:
        f.write(rendered)

    print(f"Wrote {OUTPUT_MD}")


if __name__ == "__main__":
    main()
