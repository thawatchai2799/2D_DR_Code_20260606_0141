[README.md](https://github.com/user-attachments/files/29308593/README.md)
# 2D DR Code — Recoverable-Template Enumeration and Symmetry-Group Verification

Companion source code for the paper:

> **On the Equivalence Classes of Recoverable Patterns in DR Code: A Group-Theoretic Analysis with Applications to Storage Optimization**
> T. Chomsiri and W. Sriphum, *Symmetry* (MDPI).

This repository is reference **[29]** of the paper. It contains the open-source
programs that (a) enumerate every recoverable 3×3 DR Code template and (b) verify
the symmetry-group structure used throughout the analysis.

---

## Where the files are

The enumerator `DR15.py` and the verification script `verify_2d_group.py`
(together with a line-by-line code walkthrough) are located in the

```
/Response_to_Reviewers/
```

folder of this repository:

| File | Path |
|------|------|
| `DR15.py` | [`/Response_to_Reviewers/DR15.py`](Response_to_Reviewers/DR15.py) |
| `verify_2d_group.py` | [`/Response_to_Reviewers/verify_2d_group.py`](Response_to_Reviewers/verify_2d_group.py) |
| `DR15_code_explained.html` | [`/Response_to_Reviewers/DR15_code_explained.html`](Response_to_Reviewers/DR15_code_explained.html) |

Both scripts use **only the Python standard library** (no third-party packages)
and run on Windows, Linux, and macOS with Python 3.

---

## What each file does

### `DR15.py` — recoverable-template enumerator (Theorem 1)

Exhaustively examines all `9! = 362,880` placements of the nine logical blocks on
the 3×3 grid and keeps the ones that satisfy the recoverability constraint of
**Definition 1** (every row and every column carries exactly one block from each
recovery group). It reports:

- the exact count of recoverable templates — **2,592** — confirming **Theorem 1**;
- an independent analytical cross-check `12 × (3!)³ = 2,592` (the Theorem 1 proof:
  12 order-3 Latin squares × role assignments), used for the breakdown in **Table 1**;
- a worked demonstration of the **Recovery Theorem** (strip recovery by index-wise
  XOR `Cᵢ = Aᵢ ⊕ Bᵢ`) on the original Sriphum (2013) template;
- the full enumeration written to `DR_Code.txt` (one template per record).

Run:

```bash
python DR15.py
```

### `verify_2d_group.py` — symmetry-group structure verification (Theorem 7)

Realises the five generators (Mirror σ_M, Flip σ_F, 90°-Rotation σ_R, row-shift σ_W,
column-shift σ_C) as permutations of the nine grid cells, builds the closure by
breadth-first search, and verifies the group structure claimed in **Theorem 7**:

- `|G| = 72`;
- `D₄ = ⟨σ_M, σ_F, σ_R⟩` has order 8; `N = ⟨σ_W, σ_C⟩ ≅ C₃ × C₃` has order 9;
- `N` is **normal** in `G`, `D₄` is **not** normal;
- `D₄ ∩ N = {e}` and `N · D₄ = G` (internal product cover);
- `D₄` does **not** commute with `N`, with the explicit witness
  `σ_R · σ_W · σ_R⁻¹ = σ_C⁻¹` (a 90° rotation swaps the row- and column-shifts);
- the structure homomorphism `φ : D₄ → Aut(N) = GL(2, GF(3))` together with its
  matrices and a faithfulness (trivial-kernel) check.

The combined result establishes

```
G ≅ (C₃ × C₃) ⋊ D₄     (semi-direct product)
  ≇ D₄ × C₃ × C₃        (the direct product is refuted),
```

both of order 72, so every orbit count in the paper (36 under `G`, 324 under `D₄`,
288 under the cyclic subgroup) is unaffected — only the structural claim changes.
These are the checks supporting **Theorem 7** and the equivalence-class counts of
**Tables 1–4** and **Figures 7–8**.

Run:

```bash
python verify_2d_group.py
```

### `DR15_code_explained.html` — code walkthrough (supplementary)

A self-contained HTML document that explains `DR15.py` section by section
(data model, Definition 1, enumeration loop, recovery demonstration). Open it in
any web browser. This file is supplementary documentation and is not required to
reproduce the results.

---

## Reproducing the paper's headline numbers

```bash
python DR15.py            # -> "Recoverable DR Code templates: 2592"
python verify_2d_group.py # -> "|G| = 72" and the full semi-direct-product verification
```

Both scripts are deterministic and finish in well under a second on a typical
laptop.

---

## Citation

```
T. Chomsiri and W. Sriphum, "DR15.py: open-source enumerator of recoverable
2D DR Code templates," GitHub repository, 2026.
https://github.com/thawatchai2799/2D_DR_Code_20260606_0141
```
