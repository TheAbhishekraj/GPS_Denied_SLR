#!/usr/bin/env python3
"""Validate screening prompts and AI response files for the 2010-2026 SLR."""

import json
import re
import sys
from pathlib import Path

ROOT = Path("E:/GPS_Denied_SLR")
PROMPT_DIR = ROOT / "03_prompts/screening_prompts"
RESPONSE_DIR = ROOT / "04_ai_responses/screening"


def numbered_files(directory: Path, pattern: str, expression: str) -> dict[int, Path]:
    result = {}
    for path in directory.glob(pattern):
        match = re.search(expression, path.name)
        if match:
            result[int(match.group(1))] = path
    return result


def main() -> int:
    prompts = numbered_files(PROMPT_DIR, "screening_*.txt", r"screening_(\d+)")
    responses = numbered_files(RESPONSE_DIR, "resp_*.json", r"resp_(\d+)")
    expected = set(prompts)
    response_numbers = set(responses)
    errors: list[str] = []

    if not prompts:
        errors.append("No screening prompts found.")
    if len(prompts) != len(set(prompts)):
        errors.append("Duplicate prompt numbers detected.")

    for number, path in sorted(prompts.items()):
        content = path.read_text(encoding="utf-8")
        if "Published 2010–2026" not in content and "Published 2010-2026" not in content:
            errors.append(f"{path.name}: missing 2010-2026 criterion")

    for number, path in sorted(responses.items()):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"{path.name}: invalid JSON ({exc})")
            continue
        if data.get("paper_number") != number:
            errors.append(f"{path.name}: paper_number={data.get('paper_number')!r}")
        if data.get("decision") not in {"INCLUDE", "EXCLUDE"}:
            errors.append(f"{path.name}: invalid decision")
        if data.get("confidence") not in {"High", "Medium", "Low"}:
            errors.append(f"{path.name}: invalid confidence")

    missing = sorted(expected - response_numbers)
    unexpected = sorted(response_numbers - expected)
    if missing:
        errors.append(f"Missing responses: {len(missing)}")
        print(f"Missing responses: {len(missing)} (first: {missing[:10]})")
    if unexpected:
        errors.append(f"Responses without prompts: {unexpected[:10]}")

    print(f"Prompts: {len(prompts)}")
    print(f"Responses: {len(responses)}")
    print(f"Complete: {len(expected) > 0 and not missing}")
    print(f"Validation errors: {len(errors)}")
    for error in errors[:20]:
        print(f"ERROR: {error}")

    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
