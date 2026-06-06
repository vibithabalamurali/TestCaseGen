import re
from pathlib import Path

from services.gherkin_formatter import format_for_cucumber_behave

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "output"


def _slugify(name: str) -> str:
    slug = re.sub(r"[^\w\s-]", "", name.lower())
    slug = re.sub(r"[\s_-]+", "_", slug).strip("_")
    return slug or "generated_feature"


def write_feature_file(gherkin: str, feature_name: str, output_path: Path | None = None) -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    formatted = format_for_cucumber_behave(gherkin, feature_name)

    if output_path is None:
        filename = f"{_slugify(feature_name)}.feature"
        output_path = OUTPUT_DIR / filename
    else:
        output_path = Path(output_path)
        if output_path.suffix != ".feature":
            output_path = output_path.with_suffix(".feature")
        output_path.parent.mkdir(parents=True, exist_ok=True)

    output_path.write_text(formatted, encoding="utf-8")
    return output_path.resolve()
