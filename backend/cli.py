#!/usr/bin/env python
"""CLI: paste a user story → generate Gherkin test cases → write a .feature file."""

import argparse
import sys
from pathlib import Path

from services.generator import generate_test_cases
from services.feature_writer import write_feature_file, OUTPUT_DIR

SAMPLE_STORY = """As a registered user,
I want to log in with my email and password,
So that I can access my account dashboard.

Acceptance Criteria:
- Valid email and password grant access
- Invalid credentials show an error message
- Account locks after 5 failed attempts within 15 minutes
- Empty fields show validation errors"""


def main():
    parser = argparse.ArgumentParser(
        description="Generate Gherkin test cases from a user story (Cucumber/Behave ready)",
    )
    parser.add_argument("-s", "--story", help="User story text")
    parser.add_argument("-f", "--file", type=Path, help="Read user story from a text file")
    parser.add_argument(
        "-o", "--output",
        type=Path,
        help=f"Output .feature file path (default: {OUTPUT_DIR}/<feature_name>.feature)",
    )
    parser.add_argument("--sample", action="store_true", help="Use built-in sample user story")
    parser.add_argument("--no-save", action="store_true", help="Print to stdout only, do not write file")
    args = parser.parse_args()

    if args.sample:
        user_story = SAMPLE_STORY
    elif args.file:
        if not args.file.exists():
            print(f"Error: file not found: {args.file}", file=sys.stderr)
            sys.exit(1)
        user_story = args.file.read_text(encoding="utf-8")
    elif args.story:
        user_story = args.story
    else:
        print("Enter your user story (press Ctrl+Z then Enter on Windows, or Ctrl+D on Unix to finish):\n")
        user_story = sys.stdin.read()

    if not user_story.strip():
        print("Error: user story is empty", file=sys.stderr)
        sys.exit(1)

    try:
        result = generate_test_cases(user_story)
        gherkin = result["gherkin"]

        print(gherkin)
        print()

        if not args.no_save:
            file_path = write_feature_file(gherkin, result["feature_name"], args.output)
            print(f"Saved: {file_path}")

    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)
    except Exception as exc:
        print(f"Generation failed: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
