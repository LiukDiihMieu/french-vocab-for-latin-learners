#!/usr/bin/env python3
import pathlib

import yaml
from jinja2 import Environment, FileSystemLoader


ROOT = pathlib.Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "nouns.yaml"
TEMPLATE_DIR = ROOT / "templates"
OUTPUT_DIR = ROOT / "build"
OUTPUT_MD = OUTPUT_DIR / "vocab.md"


def main() -> None:
    # Load YAML
    with DATA_PATH.open("r", encoding="utf-8") as f:
        entries = yaml.safe_load(f)

    # Sort by index just in case
    entries = sorted(entries, key=lambda e: e["index"])

    # Jinja2 environment
    env = Environment(
        loader=FileSystemLoader(str(TEMPLATE_DIR)),
        autoescape=False,
        trim_blocks=True,
        lstrip_blocks=True,
    )
    template = env.get_template("vocab.md.j2")

    # Render Markdown
    rendered = template.render(entries=entries)

    # Ensure build dir exists
    OUTPUT_DIR.mkdir(exist_ok=True)

    # Write markdown
    with OUTPUT_MD.open("w", encoding="utf-8") as f:
        f.write(rendered)

    print(f"Wrote {OUTPUT_MD}")


if __name__ == "__main__":
    main()
