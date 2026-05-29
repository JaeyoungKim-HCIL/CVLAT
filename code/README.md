# Code Supplementary

Prompt templates and an inference example.

## Files

- `prompts.json` — Seven prompt strings: `normal`, `anon_baseline` (identical to `normal`, kept as a separate key for clarity), `explain`, `visual_priority`, `factual_priority`, `q_only`, and `answer_extraction_judge`.
- `example_inference.py` — Runs one CVLAT trial on a single model and extracts a letter answer (a GPT judge maps the free-form response to a letter).
- `requirements.txt` — Python dependencies.

## Which prompt is used where

| Experiment / Cell | Prompt |
|---|---|
| Experiment 1, VLAT/reVLAT, Normal | `normal` |
| Experiment 1, VLAT/reVLAT, Explain | `explain` |
| Experiment 2, CVLAT conflict cell | `normal` |
| Experiment 2, anonymized-baseline (V_anon) | `anon_baseline` |
| Experiment 2, Q-only (F_Q) | `q_only` |
| Experiment 3, factual-priority | `factual_priority` |
| Experiment 3, visual-priority | `visual_priority` |
| Answer extraction judge | `answer_extraction_judge` |

## Quickstart

```bash
pip install -r requirements.txt
export OPENROUTER_API_KEY='sk-or-...'
python example_inference.py
```

By default the script loads `CVLAT/image/100_stacked_bar_chart.png` and question `"1"` from `CVLAT/QAset/100_stacked_bar_chart_QAset.json`, sends them to Gemini-3.1-Flash-Lite under the `normal` prompt, and prints the result. Edit the `MODEL`, `CHART_TYPE`, `QUESTION_NO`, and `PROMPT_KEY` constants at the top of the script to try other configurations. Inference uses temperature = 0 throughout.
