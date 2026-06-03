# CVLAT: Counterfactual Visualization Literacy Assessment Test

[![arXiv](https://img.shields.io/badge/arXiv-2606.03142-b31b1b.svg)](https://arxiv.org/abs/2606.03142)

This repository accompanies the paper:

> **Disentangling Visual and Factual Correctness in LVLMs' Visualization Literacy** <br>
> Soohyun Lee\*, Jaeyoung Kim\*, Seokhyeon Park, Sihyeon Lee, Jiwon Song, Bohyoung Kim, Hyunjoo Song, Jinwook Seo <br>
> *IEEE Transactions on Visualization and Computer Graphics (TVCG), under review.* <br>
> (\*co-first authors)
>
> 📄 arXiv: [2606.03142](https://arxiv.org/abs/2606.03142)

This repository contains visualization images and question-answer sets for the
visualization literacy benchmarks used in our paper — **CVLAT** (ours), **VLAT**, and
**reVLAT** — along with prompt templates and an inference example.

CVLAT is a diagnostic benchmark for measuring **visual–factual arbitration** within
LVLMs' visualization literacy: it pairs counterfactual charts (whose encodings
deliberately contradict widely shared facts) with multiple-choice questions, letting us
measure whether a model follows the **visual evidence** or defaults to its **factual
priors** when the two conflict.

---

## Directory structure
```
├── CVLAT/
│   ├── image/              # Visualization images
│   └── QAset/              # Question-answer sets (JSON)
├── CVLAT_Anonymized/
│   ├── image/              # Anonymized visualization images
│   └── QAset/              # Question-answer sets (JSON)
├── VLAT/
│   ├── image/              # Visualization images
│   ├── image_kwon/         # Alternative image set
│   └── QAset/              # Question-answer sets (JSON)
├── reVLAT/
│   ├── image/              # Visualization images
│   ├── image_white_bg/     # Images with white background
│   └── QAset/              # Question-answer sets (JSON)
└── code/
    ├── prompts.json
    ├── example_inference.py
    └── README.md
```
---

## Benchmark description

### CVLAT (Counterfactual Visualization Literacy Assessment Test) — ours
Our proposed benchmark: 48 questions adapted from VLAT with deliberately counterfactual
visualizations that conflict with widely-known facts. Designed to systematically assess
how LVLMs prioritize between visual information and factual knowledge. Used in Experiment 2.

### CVLAT_Anonymized — ours
Companion to CVLAT used as the anonymized-baseline cell (Section V-A4). Same charts as
CVLAT but with axis labels, legend entries, and category names replaced by neutral
letters, and entity-name choices mapped to the same letters. Used to estimate the
chart-reading capability reference `V_anon`.

### VLAT (Visualization Literacy Assessment Test)
Based on Lee et al.'s VLAT: 53 multiple-choice questions across 12 chart types, using
data that generally aligns with real-world facts. Used in Experiment 1 to establish
baseline performance.

### reVLAT (Randomized VLAT)
Adapted from Hong et al.'s reVLAT: maintains VLAT's chart and task types but uses
randomized data that contradicts or bears no relation to real-world facts. Used in
Experiment 1 to complement VLAT.

---

## Metrics

For CVLAT, each response is classified as **visually-correct**, **factually-correct**,
**distractor**, or **Omit**, from which we compute:

- **VF Score** — adherence to visual evidence, normalized by chart-reading capability (`V_anon`, from CVLAT_Anonymized).
- **FA Score** — reliance on factual priors, normalized by factual-prior availability (`F_Q`, from the Q-only condition).
- **VFRI** ∈ [−1, +1] — relative preference: **+1** = purely visual, **−1** = purely factual.

See Section V of the paper for full definitions, including the correction-for-guessing
procedure.

---

## Data format

**CVLAT, CVLAT_Anonymized** — each JSON item contains:
- `Q`: question text
- `Choices`: multiple-choice options (including an 'Omit' option)
- `VA`: visually-correct answer (derived from the counterfactual visualization)
- `FA`: factually-correct answer (based on real-world knowledge)
- `Type`: task type

**VLAT, reVLAT** — each JSON item contains:
- `Q`: question text
- `Choices`: multiple-choice options (including an 'Omit' option)
- `A`: correct answer
- `Type`: task type (e.g., Retrieve Value, Find Extremum, Determine Range, Make Comparisons)

---

## Code

The `code/` folder contains all prompt templates (`prompts.json`) and an inference
example (`example_inference.py`). See [`code/README.md`](code/README.md) for the
prompt-to-cell mapping and usage.

```bash
pip install -r code/requirements.txt
export OPENROUTER_API_KEY='sk-or-...'
python code/example_inference.py
```

---

## Citation

If you use CVLAT, please cite:

```bibtex
@article{lee2026cvlat,
  title         = {Disentangling Visual and Factual Correctness in {LVLMs}' Visualization Literacy},
  author        = {Lee, Soohyun and Kim, Jaeyoung and Park, Seokhyeon and Lee, Sihyeon and Song, Jiwon and Kim, Bohyoung and Song, Hyunjoo and Seo, Jinwook},
  journal       = {arXiv preprint arXiv:2606.03142},
  eprint        = {2606.03142},
  archivePrefix = {arXiv},
  year          = {2026},
  note          = {Under review at IEEE TVCG}
}
```
*(Update with the final DOI / volume / pages once published.)*

---

## Acknowledgements & third-party materials

This repository builds on prior visualization literacy benchmarks. Charts derived from
these remain subject to their original terms; please cite the original works when using
those materials.

- VLAT — Lee et al., 2016: https://ieeexplore.ieee.org/abstract/document/7539634/
- reVLAT — Hong et al., 2025 (original repo): https://github.com/VADERASU/llm4viz-experiments

---

## License

- **Code** (`code/`): [MIT License](LICENSE).
- **CVLAT / CVLAT_Anonymized** (charts and question sets we created): [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). See [`LICENSE-DATA.md`](LICENSE-DATA.md).
- **Third-party materials** (`VLAT/`, `reVLAT/`): derived from prior benchmarks
  (see Acknowledgements) and **not** covered by the licenses above; they remain subject to
  their original sources and are included only for research reproducibility.

---

## Contact

For questions about CVLAT, contact the co-first authors:
Soohyun Lee (shlee@hcil.snu.ac.kr) and Jaeyoung Kim (jaeyoung.kim.cs@gmail.com).
