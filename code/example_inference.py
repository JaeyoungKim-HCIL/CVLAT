"""Run one CVLAT trial on a single LVLM via OpenRouter, then extract the
letter answer with a GPT judge.
"""

from __future__ import annotations

import base64
import json
import os
import sys
from pathlib import Path

from openai import OpenAI


MODEL = "google/gemini-3.1-flash-lite"   # cheap multimodal model for the example
JUDGE_MODEL = "openai/gpt-5.4-nano"

CVLAT_ROOT = Path(__file__).resolve().parent.parent / "CVLAT"
CHART_TYPE = "100_stacked_bar_chart"
QUESTION_NO = "1"
PROMPT_KEY = "normal"

PROMPTS = json.loads((Path(__file__).parent / "prompts.json").read_text())
LETTERS = ["(a)", "(b)", "(c)", "(d)", "(e)"]


def image_to_data_url(image_path: Path) -> str:
    return "data:image/png;base64," + base64.b64encode(image_path.read_bytes()).decode()


def format_user_message(item: dict) -> str:
    lines = [item["Q"], ""]
    for letter, choice in zip("abcde", item["Choices"]):
        lines.append(f"({letter}) {choice}")
    return "\n".join(lines)


def text_to_letter(choices: list[str], target_text: str) -> str:
    try:
        return LETTERS[choices.index(target_text)]
    except ValueError:
        return "Unknown"


def call_target_model(client: OpenAI, system_prompt: str,
                      user_text: str, image_data_url: str) -> str:
    resp = client.chat.completions.create(
        model=MODEL,
        temperature=0.0,
        messages=[
            {"role": "system",
             "content": [{"type": "text", "text": system_prompt}]},
            {"role": "user",
             "content": [
                 {"type": "text", "text": user_text},
                 {"type": "image_url", "image_url": {"url": image_data_url}},
             ]},
        ],
    )
    return resp.choices[0].message.content or ""


def call_judge(client: OpenAI, raw_response: str) -> str:
    resp = client.chat.completions.create(
        model=JUDGE_MODEL,
        temperature=0.0,
        messages=[
            {"role": "system", "content": PROMPTS["answer_extraction_judge"]},
            {"role": "user", "content": raw_response},
        ],
    )
    return (resp.choices[0].message.content or "").strip()


def main() -> int:
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        sys.exit("Set OPENROUTER_API_KEY before running this script.")

    client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)

    qaset = json.loads((CVLAT_ROOT / "QAset" / f"{CHART_TYPE}_QAset.json").read_text())
    if QUESTION_NO not in qaset:
        sys.exit(f"Question '{QUESTION_NO}' not in {CHART_TYPE}_QAset.json")

    item = qaset[QUESTION_NO]
    system_prompt = PROMPTS[PROMPT_KEY]
    user_text = format_user_message(item)
    image_url = image_to_data_url(CVLAT_ROOT / "image" / f"{CHART_TYPE}.png")

    raw = call_target_model(client, system_prompt, user_text, image_url)
    extracted_letter = call_judge(client, raw)

    visual_letter = text_to_letter(item["Choices"], item["VA"])
    factual_letter = text_to_letter(item["Choices"], item["FA"])
    label = (
        "Visual"  if extracted_letter == visual_letter  else
        "Factual" if extracted_letter == factual_letter else
        "FALSE"   # everything else (distractor, Omit, Unknown) is lumped here,
                  # matching the per-trial classification used by the full runner.
    )

    print(json.dumps({
        "model": MODEL,
        "chart_type": CHART_TYPE,
        "question_no": QUESTION_NO,
        "prompt_key": PROMPT_KEY,
        "question": item["Q"],
        "choices": item["Choices"],
        "visual_correct_text": item["VA"],
        "factual_correct_text": item["FA"],
        "visual_correct_letter": visual_letter,
        "factual_correct_letter": factual_letter,
        "raw_response": raw,
        "extracted_letter": extracted_letter,
        "category": label,
    }, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
