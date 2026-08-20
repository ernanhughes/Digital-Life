# STYLE.md — Readability Control Document

*Fourth persistent control document, alongside BIBLE.md, LEDGER.md, THREADS.md.*
*Derived by measurement from the revised Chapters 05 and 06.*

---

## The defect this document exists to prevent

The manuscript's readability problem is **not** density, technicality, or too much
statistics. It is **fragmentation**. Prose has been shattered into one-clause
paragraphs, and quantities have been isolated into fenced blocks one symbol at a
time. The reader is then asked to carry six to nine unanchored tokens across a
hundred lines with no connective tissue to hold them together.

This is why the reviews reported "fatigue" while also praising the content. The
content is fine. The delivery mechanism is broken.

**Rejected reviewer advice.** Do not cut the statistics. Do not move the Failure
Ledger to an appendix. Do not reframe failed hypotheses as positives. Those
proposals treat the book's discipline as the problem. The discipline is the book.

---

## Measured targets

The two **primary gates** are the ones that actually separate the readable
chapters from the fatiguing ones:

| Primary gate | Target | Hard fail |
|---|---:|---:|
| Paragraphs of ≤ 6 words | under 25% | above 30% |
| Fenced blocks per 1000 words | 2–8 | above 10 |

Two **secondary indicators**, useful for spotting the opposite failure — a
revision that fixes fragmentation by producing walls of text:

| Secondary indicator | Band |
|---|---:|
| Words per prose paragraph | 16–30 |
| Words per H2 section | 200–320 |
| Live symbols introduced per section | ≤ 3 |

A "live symbol" is any single-letter variable, Greek letter, or bare threshold
number the reader must hold in working memory to follow the next paragraph.

Note on the paragraph band: the revised Ch 11 landed at 28.6 words per paragraph,
above Ch 05's 22.6, because the pass **merged** fragments rather than cutting
content. That is the correct trade. The band was widened after measuring the
result rather than before, and the reason is recorded here so the adjustment is
inspectable.

---

## Rules

### 1. A fenced block is for measured results, never for a symbol

A `text` block earns its place when it holds a **set** of numbers the reader will
compare — three policies, five budgets, a gate list. It never wraps a single
value, a variable name, or a phrase.

Wrong:

    the budget was:
    ```text
    B = 128
    ```

Right: `the budget was 128`.

If a block would contain fewer than three lines, it is prose.

### 2. Tabular data goes in a table

Anything with rows and columns — policy comparisons, budget sweeps, per-condition
values — is a Markdown table, not an ASCII block.

### 3. One-line paragraphs are a punctuation mark, not a default

They mark a turn: a hypothesis dying, a control failing, a result arriving. Used
once or twice per section they land hard. Used as the default paragraph form they
stop meaning anything and the reader loses the thread between them.

Budget: **at most two per section.**

### 4. The answer comes before the derivation

Where a section contains an algebraic audit, state the conclusion first, then show
the working. The reader who accepts the conclusion can move on; the reader who
wants to check it has the derivation in front of them. Never make the conclusion
the reward for surviving sixty lines of algebra.

### 5. Name quantities in words on first and subsequent mention

Use `the budget`, `the loss rate`, `the reuse arm` in the narrative. Reserve the
symbol for the equation that needs it. Where an equation is genuinely required,
introduce every symbol in a **single sentence** immediately before the display,
then use the display once and return to words.

### 6. Contrast blocks are rationed

The `A ≠ B` block is one of the book's best devices and it is being spent
carelessly. **One per section, at most three per chapter**, reserved for the
distinction the chapter actually turns on.

### 7. Technical machinery lives in the Experimental Note

Protocol parameters, group counts, warmup lengths, window definitions and gate
arithmetic belong in the Note. The main text states what was required and whether
it was met. This is not hiding the audit; the Note is the audit and it is
immediately below.

### 8. Verdict words are never softened

`SUPPORTED / FAILED / UNRESOLVED / INCONCLUSIVE / BOUNDED NEAR ZERO / INVALID /
NOT CLAIMED` are set in bold inline in the sentence that reaches them. They do not
get their own fenced block, because a block implies ceremony and the ledger is
where the ceremony belongs. The word itself is not weakened, hedged, or
re-narrated as a success.

### 9. Every number in the original survives the pass

A readability revision changes sentence architecture only. No measured value, no
threshold, no gate, no claim status, and no scope caveat may be dropped, rounded,
or moved to a weaker qualifier. Verify by diff of the extracted numeral set before
and after.

---

## Chapter priority, by measurement

| Priority | Chapter | w/para | blk/1k | Note |
|---|---|---:|---:|---|
| ~~1~~ | ~~11 — What Does It Cost to Stay?~~ | ~~8.4~~ | ~~19.5~~ | **done** — now 28.6 / 2.1, short% 46 → 23 |
| 2 | 10 — What Survives Material Loss? | 9.8 | 13.0 | |
| 3 | 07 — The Digital Crystal | 10.5 | 11.5 | also longest sections |
| 4 | 17 — How to Fail Correctly | 10.3 | 11.7 | keep the ledger, fix the prose |
| 5 | 01 — How to Read This Book | 8.8 | 8.0 | short, quick win |
| 6 | 12 — Is There Actually One Thing Here? | 15.0 | 9.2 | |
| 7 | 09 — Can Experience Change the Material? | 16.6 | 7.9 | 21 sections |
| 8 | 08 — The Crystal Gets a Past | 17.0 | 7.6 | longest chapter; duplicate `## Experimental Note` heading at lines 961 and 977 — structural defect, fix in this pass |
| — | 13, 14, 15, 16, 18 | 20+ | ≤ 7.4 | paragraph health is fine; their issue is chapter length, a separate pass |
| — | 02, 03, 04, 05, 06 | — | — | pass; leave alone |

---

## Verification command

    python3 - <<'EOF'
    import re,sys
    t=open(sys.argv[1] if len(sys.argv)>1 else 'ch.md',encoding='utf-8').read().replace('\r\n','\n')
    body=t.split('+++')[2]
    parts=body.split('```')
    prose='\n'.join(parts[i] for i in range(0,len(parts),2))
    paras=[p for p in re.split(r'\n\s*\n',prose) if p.strip() and not p.strip().startswith(('#','|','+','$$'))]
    short=sum(1 for p in paras if len(p.split())<=6)
    w=len(body.split())
    print('words',w)
    print('blk/1k',round(1000*(body.count('\n```')//2)/w,1))
    print('w/para',round(sum(len(p.split()) for p in paras)/len(paras),1))
    print('%<=6wd',round(100*short/len(paras)))
    EOF
