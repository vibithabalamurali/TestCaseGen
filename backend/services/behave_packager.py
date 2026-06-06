import io
import zipfile
from pathlib import Path

from services.gherkin_formatter import format_for_cucumber_behave
from services.behave_templates import (
    BEHAVE_INI,
    COMMON_STEPS_PY,
    ENVIRONMENT_PY,
    README_BEHAVE,
    README_CUCUMBER,
)


def build_behave_package(gherkin: str, feature_filename: str, feature_name: str = "") -> bytes:
    """Build a ZIP containing a Behave-ready project + Cucumber instructions."""
    formatted = format_for_cucumber_behave(gherkin, feature_name)
    safe_name = Path(feature_filename).name
    if not safe_name.endswith(".feature"):
        safe_name = f"{safe_name}.feature"

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("behave.ini", BEHAVE_INI)
        zf.writestr("features/environment.py", ENVIRONMENT_PY)
        zf.writestr("features/steps/common_steps.py", COMMON_STEPS_PY)
        zf.writestr(f"features/{safe_name}", formatted)
        zf.writestr("README_BEHAVE.md", README_BEHAVE)
        zf.writestr("README_CUCUMBER.md", README_CUCUMBER)

    zip_buffer.seek(0)
    return zip_buffer.read()


def package_filename(feature_filename: str) -> str:
    stem = Path(feature_filename).stem
    return f"{stem}_cucumber_behave.zip"
