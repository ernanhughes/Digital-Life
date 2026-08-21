+++
title = "17: How to Fail Correctly"
date = "2026-08-15T03:00:00+01:00"
draft = false
description = "The strongest controls in this investigation repeatedly destroyed richer interpretations while leaving smaller phenomena intact. This chapter makes explicit the bookkeeping required to fail one claim without erasing what the evidence still supports."
weight = 17
categories = ["Programming", "Artificial Life"]
tags = ["Digital Life", "Digital Crystal", "Experimental Method", "Epistemology"]
series = ["Digital Life From First Principles"]
has_colab = true
chapter_status = "review"
+++

The most dangerous result in this book was not a noisy one.

It was one of the cleanest.

```text
measurement            ✓    M = 0.4402
                            CI [0.419, 0.461]

precision              ✓    MDE80 = 0.0268
                            against a +0.15 threshold

implementation         ✓    corrected transient intervention
                            known global channels removed

predeclaration         ✓    regions selected blind to outcome
                            threshold frozen

fresh reproduction     ✓    selected regions scored 0.4436
                            in an independent matched-null run

individuation          ✕    not established
```

The two numbers come from different runs. V1 measured raw causal containment on seed `20260916`. V2 regenerated the selected regions on fresh seed `20260917`, reproduced the raw score at `0.4436`, and then asked the stronger question: did those regions exceed same-checkpoint matched controls?

Many of the safeguards we had learned to trust were satisfied. The number was large. The interval was narrow. The intervention was correct. The region selection was outcome-blind. The raw phenomenon appeared again on a fresh seed.

And the inference from strong causal containment to causal individuality still did not survive the geometry-matched control.

The measurement was right. What we thought it meant was not.

That is worth sitting with, because it exposes the limits of procedural rigour.

Predeclaration can stop us moving a threshold after seeing the answer; it cannot guarantee that we chose the right threshold, the right estimand, or the right null. Precision can tell us how tightly we measured a quantity; it cannot tell us whether that quantity identifies the construct we care about. A corrected implementation can make an experiment internally valid; it cannot guarantee that the valid experiment asks the scientifically important question.

So before the final chapter asks what survived this investigation, this one has to make explicit the bookkeeping that determined what was allowed to survive. The book has been doing that bookkeeping implicitly for most of its experimental life. Now it needs to be stated.

> **When a claim fails, what exactly has failed?**

---

## Failure Is Not One Thing

The word *failure* compresses several situations that license completely different conclusions.

An experiment may never have implemented the contrast it claimed to test. A valid experiment may have been too imprecise to answer its own question. A valid and sufficiently precise experiment may exclude an effect large enough to matter. A lower-level phenomenon may be measured cleanly while the richer interpretation attached to it collapses under a stronger control. A follow-up analysis may explain something interesting without being allowed to alter the status of the confirmatory test.

These are not different degrees of the same outcome. They live at different logical levels.

Four terms do most of the work from here, and it is worth fixing them before they start carrying weight.

| Term | Meaning |
|---|---|
| **estimand** | the specific quantity an experiment is built to estimate |
| **construct** | the richer theoretical concept we hope that quantity helps identify |
| **SEI** | smallest effect of interest — the predeclared magnitude that counts as scientifically meaningful for that estimand |
| **MDE80** | the achieved minimum detectable effect at 80% power, under the frozen analysis convention |

The gap between the first two is where most of this chapter lives. An estimand is something an experiment can deliver. A construct is something we decide the estimand licenses us to say.

The statuses themselves sit at four different levels, and conflating those levels is how the bookkeeping goes wrong.

| Level | Status | Meaning |
|---|---|---|
| run validity | **INVALID** | the run cannot support the intended estimand, because its intervention, implementation, operationalization or reference contrast is defective |
| inferential status | **UNRESOLVED** | the declared question remains open at the required precision |
| | **SUPPORTED** | the tested claim survived |
| | **BOUNDED** | a predeclared effect region was excluded with adequate precision |
| evidence role | **DESCRIPTIVE ONLY** | informative follow-up that does not alter confirmatory status |
| claim transition | **NARROWED** | a lower-level result survived while a richer interpretation did not |

Even `BOUNDED` is not one thing. Two cases in this book used different forms of it: **BOUNDED NEAR ZERO**, where a declared two-sided meaningful band is resolved around zero, and **BOUNDED BELOW SEI**, where a declared positive effect of meaningful size is excluded. Those are not interchangeable.

One consequence follows immediately, and it shapes everything below. An experiment does not receive a single global status. Direction, magnitude, mechanism, construct validity and descriptive closeouts answer different claims, and each carries its own. The bookkeeping attaches a status to a claim, not to a run.

Nor is `INVALID` merely another inferential status. An invalid experiment does not produce a weak answer to the original question; it fails to instantiate the question correctly. And `NARROWED` is not a statistical verdict at all — it describes what happens when a stronger control leaves a smaller claim intact while removing permission for a larger one.

The reason for keeping these categories separate is simple:

> **A failed claim, an invalid experiment and an absent phenomenon are three different things.**

The easiest way to use the distinctions is not to memorize a taxonomy. It is to ask a sequence of questions.

---

## Did We Run the Experiment We Claimed?

The *Can the Past Redirect the Future?* chapter intended a clean contrast. Under FORCE, `x` is present for one controlled causal exposure. Under PREVENT, `x` is prevented from appearing during that same exposure.

The first implementation did not do that. FORCE inserted `x`. PREVENT merely *started* with `x` empty, which left the supposedly prevented cell eligible to attach naturally during the first update.

Worse, the probability of that contamination depended on the treatment arm. Natural PREVENT attachment of `x` occurred at `0.428` under ACCESSIBLE, `0.377` under REMOTE and `0.378` under ERASED. The hidden material state altered the probability that the supposedly prevented event would occur.

So the intended causal contrast had not been implemented, and the downstream result was **INVALID**.

The crucial point is that this verdict is logically prior to the numerical outcome. If a broken intervention returns a large effect, it is tempting to salvage it. If it returns nothing, it is tempting to report a negative result. Both are the same error: the affected estimand was never correctly instantiated.

```text
INVALID
≠
NEGATIVE
≠
UNRESOLVED
```

An invalid result is evidence neither for nor against the claim it failed to test. That sounds obvious when written down. It is much harder when the invalid run contains a result you want.

The productive question after invalidation is therefore not *can we keep the conclusion?* It is:

> **Which quantities were causally upstream of the defect?**

In that experiment, the immediate expected causal response had been computed before the contaminated growth step, so its value could not depend on whether PREVENT later allowed `x` to attach. That immediate quantity therefore survived the invalidation. It was audited separately, its negative sign was reproduced after the intervention was repaired, and it supplied the operating-point mechanism that made the otherwise surprising sign intelligible.

The downstream result disappeared. The independent immediate result stayed.

That is what failing correctly looks like.

---

## Could the Experiment Answer Its Question?

A valid experiment can still fail to resolve the question it was built to answer.

Earlier, while trying to predict downstream causal consequence from local geometry, one estimate came back at approximately `+0.167`, with a 95% confidence interval of `[-0.078, +0.431]` against a declared meaningful scale of `0.15`.

Reporting that as evidence against the hypothesis would have been a straightforward misrepresentation. The interval contains zero, but that is not the important fact. It also contains substantial positive effects well beyond the declared meaningful scale. The experiment could not distinguish a meaningful positive effect from a small effect, from zero, from an effect in the opposite direction.

The correct status was **UNRESOLVED**, not **FAILED**.

The test is not simply whether an interval contains zero. The more useful question is:

> **What scientifically meaningful effects remain compatible with the data?**

If effects at or beyond the predeclared scale of interest remain compatible with the observations — and the achieved precision cannot resolve that scale — then the magnitude question remains open. Whether the interval excludes zero can answer the directional question. Whether it excludes the predeclared effect threshold answers a different, magnitude question.

The distinction became especially clear in *Can the Past Redirect the Future?* The corrected experiment produced an ACCESSIBLE minus REMOTE mean of `−0.397`, with a 95% interval of `[−0.679, −0.119]`.

The entire interval lay below zero, so the directional question had an answer. Is the effect negative? **SUPPORTED**.

But the frozen smallest effect of interest was `±0.15`, and the achieved one-sided MDE80 was about `0.357`. The interval also extended to `−0.119`, a magnitude smaller than the declared `0.15` threshold. So the magnitude question — can we establish the predeclared minimum? — remained **UNRESOLVED**.

Those two statements are compatible.

```text
DIRECTION
≠
MAGNITUDE
```

Calling the whole result *supported* would have promoted a magnitude the experiment did not resolve. Calling the whole result *inconclusive* would have thrown away a direction the experiment did establish. Failure bookkeeping is partly the discipline of refusing both simplifications.

---

## Did We Exclude Something Worth Excluding?

The reverse mistake is just as common: an estimate close to zero gets reported as *nothing happened*.

But a small point estimate means little by itself. To make a useful negative statement, the experiment has to define what would count as meaningful and then demonstrate enough precision to exclude it. Two recent experiments did this in different ways.

| | coupling / amplification | modularity excess |
|---|---|---|
| estimate | +0.00130 | −0.0123 |
| 95% CI | [−0.08984, +0.08854] | [−0.0327, +0.0072] |
| declared threshold | ±0.15, two-sided band | +0.10, positive SEI |
| MDE80 | ≈ 0.115 | 0.0265 |
| earned status | BOUNDED NEAR ZERO | BOUNDED BELOW SEI |

In *Can Finite Computation Couple Distant Events?*, strong candidate subsampling was compared with true exhaustive evaluation under dynamically matched background construction. At twelve updates, the question was two-sided: could the mean consequence differ from exhaustive evaluation by at least `0.15` in either direction? The answer was no at the achieved precision, so that result is **BOUNDED NEAR ZERO** at the declared `±0.15` scale.

The previous chapter asked a different question. Selected regions were compared with geometry-matched controls, and the scientific claim was directional in a different sense: did the selected regions show **positive excess modularity** of at least `+0.10` beyond the matched null?

The upper confidence bound was only `+0.0072`, and the achieved precision was far tighter than the declared threshold, so meaningful positive excess is **BOUNDED BELOW SEI**. The direction around zero, however, remains **UNRESOLVED**, because the interval still crossed zero.

Two different thresholds appear in that pair of experiments, and the difference is worth stating plainly before it looks like drift. Raw modularity carried an SEI of `+0.15`; excess modularity carried an SEI of `+0.10`.

These belong to different estimands. The first froze the smallest meaningful value of raw containment. The second introduced a new quantity — excess containment over geometry-matched controls — and froze its threshold before seeing any result for it. A new estimand may legitimately carry its own predeclared threshold.

What would not be legitimate is moving an existing threshold because its answer turned out to be inconvenient. Neither number has a theoretical derivation behind it; both are declared operational thresholds, and their integrity comes entirely from having been fixed in advance.

So those two experiments earned different negative claims, and neither is the same as a bare failure to reject zero. `BOUNDED NEAR ZERO` excludes a two-sided band. `BOUNDED BELOW SEI` excludes a one-sided region. *Not significant* excludes nothing at all. Each of the first two states a scale, and that is what makes them stronger than an absence of evidence.

It also explains why precision belongs in the status. The same point estimate could be **BOUNDED** under one standard error and **UNRESOLVED** under another. A negative result is not the absence of a positive point estimate.[^altman] It is an inference about what effect sizes the experiment has actually ruled out.

[^altman]: D. G. Altman and J. M. Bland, "Absence of evidence is not evidence of absence", *BMJ* 311 (1995), 485.

---

## Does the Measurement Identify the Construct?

Now the failure that none of the previous checks can catch — and the reason this chapter exists.

The previous chapter's **raw containment measurement** was valid, and the measured phenomenon was real. At radius four, internal retention ran at about `0.776` and external penetration at about `0.335`, giving a raw modularity `M` of about `0.440`. Perturbations initiated inside the selected regions really did express much more accumulated causal effect inside those regions than comparable external perturbations expressed inward.

The number was not an artifact of a broken intervention. It was not underpowered. It was not selected after looking at the outcome. It appeared again on a fresh seed.

What failed was the promotion from that measured phenomenon to the richer construct. The layers are easier to see when separated:

| Layer | Causal modularity | Early flocking result |
|---|---|---|
| measurement | raw modularity `M ≈ 0.44` ✓ | nearby velocity coherence ✓ |
| phenomenon | strong spatial causal containment ✓ | short-range spatial motion coherence ✓ |
| construct | system-privileged causal region — **NOT ESTABLISHED** | ancestry-specific flocking — **NOT ESTABLISHED** |
| interpretation | individual — **NOT ESTABLISHED** | — |

A failure at the upper layer does not propagate automatically downward. The containment survives. The privilege claim does not.

This is a construct-validity problem. An operational quantity can be measured accurately and reproducibly while failing to uniquely identify the richer theoretical construct attached to it. The classic construct-validity literature makes the broader point that a construct is not validated by one successful association. It earns meaning through its relations to other observables and through the theoretical network of predictions surrounding it.[^cronbach]

Statistical rigour can make an estimate extremely precise. It cannot, by itself, validate the promotion from that estimate to a richer concept.

[^cronbach]: L. J. Cronbach and P. E. Meehl, "Construct validity in psychological tests", *Psychological Bulletin* 52(4) (1955), 281–302.

The experimental version of that lesson, learned repeatedly here, is:

> **Do not promote a measurement into a richer construct until a simpler mechanism capable of producing the same measurement has been controlled.**

Consider the recurring pattern:

```text
coherent motion                                → flocking
refilled vacancies                             → repair
experimentally written persistent hidden state → memory
retained causal influence                      → individual
```

In every case something real was measured. In every case the promotion was stronger than the evidence. And what exposed the mismatch was not usually a better statistic. It was a better alternative explanation.

---

## The Null Is Part of the Claim

The previous chapter makes this point sharper than any earlier example. Before the geometry-matched control, the operative inference was effectively that large raw causal modularity implies a privileged region.

The missing object in that inference was the null. How large would the same statistic be in other regions with comparable spatial and interface geometry?

Once those controls were built, selected regions scored `M ≈ 0.444` against matched controls at `M ≈ 0.456`, for an excess of about `−0.012`. The raw measurement did not disappear. Its interpretation changed.

A null is therefore not merely a ceremonial calculation applied after a result. It is part of what the result is allowed to mean.

> **A measurement is not yet evidence for a richer construct until plausible alternative generators of that measurement have been controlled.**

That pattern was already visible elsewhere. Predictive coherence weakened when ordinary structured regions were admitted into the null. Material placement weakened when copy quantity was equalized. Ancestry-specific flocking weakened when distance was matched.

Different experiments, same bookkeeping: the phenomenon survives, the promotion narrows.

---

## Fail the Smallest Claim

All of this collapses into one operating principle:

> **Fail the smallest claim the evidence actually defeats. Preserve everything that still survives.**

It rules out two opposite pathologies. The first is **over-rescue**: a rich claim weakens, so the language keeps changing until whatever remains is presented as though it were what we meant all along. That destroys the distinction between prediction and retrospective interpretation.

The second is **over-destruction**: a rich claim fails, so everything associated with it is thrown away — including measurements and mechanisms the stronger control never defeated. That feels stricter. It is not more scientific. It is simply wasteful.

The response should be surgical:

| Defect | Correct response |
|---|---|
| implementation invalid | invalidate the affected estimand only |
| precision insufficient | leave the declared question unresolved |
| meaningful effect region excluded | record the appropriate bounded result |
| stronger control defeats richer interpretation | narrow the claim |
| lower-level phenomenon remains valid | keep it |
| follow-up analysis explains or contextualizes | label it descriptive |

Applied to the three worked cases in this chapter:

| Experiment | What disappears | What stays |
|---|---|---|
| causal modularity | individual | causal containment |
| *Can the Past Redirect the Future?* | invalid V1 downstream inference | valid immediate hidden-state sensitivity |
| flocking | ancestry-specific flocking | short-range motion coherence |

This is not rhetorical moderation. It is evidence accounting.

---

## A Description Is Not a Confirmation

One category deserves separate attention, because it is the most tempting.

The corrected hidden-state experiment ended with a negative direction **SUPPORTED** and the predeclared minimum magnitude **UNRESOLVED**. Then we inspected how the effect accumulated through time, and the closeout was striking. Roughly 75% of the final cumulative difference accrued after the written material trace had fallen below half its starting mass, and about 36% accrued after it had fallen below a quarter.

That temporal pattern motivates a plausible interpretation. Early hidden-state modulation changes events; those events alter later states; later divergence may therefore depend partly on trajectory as well as on whatever material remains.

That is interesting. It is also **DESCRIPTIVE**.

The closeout was not the frozen confirmatory endpoint. It did not isolate a mediation pathway. Its pooled group-by-lag diagnostics were not independent confirmatory observations. And it cannot upgrade the unresolved minimum-magnitude claim into a supported one.

An explanation can illuminate a result without rescuing it. Calling an analysis `DESCRIPTIVE` is therefore not a dismissal — it records how the evidence was obtained and what inferential work it is allowed to do.

`DESCRIPTIVE` is not `UNIMPORTANT`, and `DESCRIPTIVE` is not `CONFIRMATORY`. Both distinctions matter.

---

## Corrections Are Not Rescues

If invalid experiments must be repaired and rerun, then rerunning an experiment cannot automatically be cheating. The distinction is in what changes.

The corrected hidden-state experiment repaired the PREVENT semantics, repaired the contaminated REMOTE comparator, and froze a lag-wise expected local causal-difference estimator before the corrected run. It kept the scientific parameters fixed — material gain, half-life, history age, horizon, effect threshold.

The scientific question remained recognizable. The instrument changed because the original instrument had not implemented that question correctly.

The computational-coupling experiment had a similar correction. A calibration scheme that controlled only the beginning of a multi-lag process was replaced by one that controlled the trajectory dynamically. Again, the repair targeted the instrument. It did not tune the scientific parameters until the desired effect appeared.

The distinctions are:

| Move | What it does |
|---|---|
| **corrective experiment** | repairs a defect in intervention, implementation, operationalization, estimand or reference contrast, while preserving the declared scientific question |
| **new experiment** | asks a materially different question, and declares that change before interpreting its result |
| **rescue** | changes the estimand, threshold, parameter regime or interpretation because the original answer was inconvenient, while presenting the new result as though it answered the old question |

The first two are legitimate scientific moves. The third is dangerous because it lets a question mutate invisibly.

---

## Knowing When to Stop

After a weakened claim, there is always another variant available. Another radius, another feature, another budget, another history window, another matching rule, another decoder, another horizon.

The search space has no natural end. That makes stopping a scientific act.

Several chapters reached points where continuing the same search would have turned disappointment into parameter hunting.

The material-placement experiments abandoned a broad line after repeated controls collapsed its richer interpretations, rather than continuing until one secondary metric looked favourable. The boundary experiments did not retune the radius after the geometric null weakened the claim. The causal-gain work stopped adding local predictors when the local prediction programme stopped earning information, and changed the measurement instead. The previous chapter changed the null rather than changing the modularity statistic until the selected regions won.

The stop rule that emerges is:

> **When the declared question has been answered, stop. Do not convert disappointment into a parameter search unless you are willing to declare a genuinely new experiment.**

The companion rule came from an earlier stationarity threshold that missed by roughly `0.00002`. Scientifically tiny. Procedurally decisive.

> **A threshold that moves when the answer is inconvenient is not a threshold.**

That can feel absurdly rigid when the miss is microscopic. But a frozen boundary is useful precisely because it prevents us deciding, after seeing the number, whether this particular miss *really counts*. The correct response is not to pretend `0.00002` matters biologically. It is to report a near miss and keep the rule intact.

---

## Auditing the Bookkeeping

Rules written in prose are cheap. The question is whether the project actually followed them.

So the most recent experimental chains were encoded into an executable failure ledger. This chapter does not introduce another Digital Crystal simulation; its experimental object is the evidence history itself.

Ten cases were registered across three recent experimental chains — finite-selector amplification, hidden-state causal response, and causal modularity and individuation — and every registered case resolved to source artifacts.

```text
registered cases             10
source-backed cases          10
manual-evidence-only          0
missing required sources      0
```

Each entry records the claim under test, the run validity, the inferential status, the transition type, the evidence role, the threshold where applicable, the achieved precision where applicable, and what evidence survived.

The audit then checks for the forbidden moves. Did an INVALID run ever become evidence against a hypothesis? Did UNRESOLVED quietly become FAILED? Did a bounded result lack a declared threshold or adequate precision? Did a stronger control erase valid lower-level evidence? Did a descriptive closeout upgrade a confirmatory claim? Did a materially changed estimand masquerade as the original one?

All ten registered cases passed the bookkeeping rules. Five cross-case checks were declared as well, and all five passed:

| Check | Required bookkeeping | Result |
|---|---|---|
| Invalid hidden-state primary | preserve the independent immediate result | PASS |
| Direction vs magnitude | keep the two statuses separate | PASS |
| Stronger spatial null | narrow the construct, preserve raw containment | PASS |
| Bounded amplification | preserve the mechanistic routing result | PASS |
| Descriptive closeout | do not rescue the magnitude claim | PASS |

The failure-ledger bookkeeping is therefore **consistent**.

Every registered case resolved to primary project artifacts — generated reports, structured result files and analysis outputs — rather than to prose recollection. A case that could only be evidenced from documented prose would have been recorded as manual-evidence-only; none were. The complete machine-readable ledger and artifact audit are retained with this chapter's research outputs, and the table above shows the cross-case checks that matter for the argument here.

That status is narrow. The ledger does not certify the truth of the conclusions, the completeness of the taxonomy, the completeness of the underlying case record, or the absence of mistakes. It checks one thing: whether the registered evidence transitions were carried forward without silently changing their logical status.

A word about the other labels that appear in the Evidence Ledgers throughout the book.

`NOT ESTABLISHED`, `NOT CLAIMED` and `UNTESTED` are scope markers rather than inferential outcomes — they record where a claim was never taken, not how an experiment turned out. `ASSERTION` and `IDENTITY` refer to implementation correctness or algebraic properties of the code, not to empirical population findings. Keeping those apart from `SUPPORTED`, `UNRESOLVED` and `BOUNDED` is part of the same discipline.

> **Across the three registered case chains — finite-selector amplification, hidden-state causal response, and causal modularity — the recorded invalidations, unresolved questions, bounded results, descriptive closeouts and claim narrowings can be represented without silently converting one evidence class into another or deleting surviving evidence.**

That is enough. A final chapter built from “what survived” is meaningless if the survival criteria changed every time a result became inconvenient.

The ledger does not certify the conclusions. It certifies the bookkeeping used to carry them forward.

---

## What All Those Failures Discovered

Here is the part that makes this chapter something other than an apology.

The failures were productive. Not in the consoling sense that every setback teaches us something, but because each one forced a distinction between concepts that had previously been allowed to blur together.

```text
similarity
≠
causal ancestry

visible state
≠
complete causal state

causal state difference
≠
readable record of a past

persistent
≠
locally accessible

accessible
≠
differentially used

net population change
≠
gross construction and loss

reoccupation
≠
repair

stable population size
≠
absence of turnover

locality
≠
privileged boundary

causal effect
≠
stable local predictor of downstream consequence

causal routing
≠
causal amplification

hidden-state conditioning
≠
record reading

causal containment
≠
causal individuation
```

Most of those distinctions were not part of the vocabulary we started with. They became necessary when a richer interpretation encountered a control that left a smaller phenomenon intact.

> **A failed promotion is a successful distinction.**

That may be the most useful way to read the investigation. We repeatedly asked questions in biological vocabulary, and the controls kept forcing the answers into narrower computational terms.

| we asked | what survived |
|---|---|
| flocking? | short-range motion coherence |
| memory? | hidden-state causal sensitivity |
| repair? | rapid reoccupation after vacancy |
| stable body size? | compute-constrained scale with substantial turnover |
| individual? | strong spatial causal containment |

The right-hand column is not a list of consolation prizes. Those are the measurements that remained after the stronger names stopped being defensible. The method's job was never to preserve the biological vocabulary. It was to discover when that vocabulary stopped earning its keep.

And the temptation was never abstract. A trace that persists really does beg to be called memory. A hole that fills really does look like healing. A population that stays roughly stable really does resemble a maintained body. A modularity score of `0.44` really did look like an individual.

The richer words were not foolish hypotheses. They were hypotheses. The mistake would have been refusing to give them up when the controls said otherwise.

---

## What Survived

Many of the stronger biological or organism-like promotions have now been removed, bounded, narrowed or left unestablished. Among them:

```text
ancestry-specific flocking

readable memory

repair

stable organism-like body size

a privileged body boundary

causal amplification

causal individuality
```

Their scientific statuses are not identical. Some failed specific controls. Some were never established in the first place. Some became unresolved at the declared magnitude. Some were replaced by narrower descriptions.

What they share is only this: none survived in the richer form initially suggested by the measurement.

What remains is not nothing. It is a list of phenomena that survived implementation audits, matched nulls, precision gates and failed interpretations:

```text
causal reproduction without an explicit reproduction operator

short-range motion coherence

counterfactual continuation from complete saved state

hidden state that can modulate causal response
without evidence that the state is a readable record

persistent material state that remains causally active
while locally accessible

loss-generated construction interfaces
and rapid reoccupation

large gross turnover concealed beneath
much smaller net population change

process scale strongly constrained
by finite computational opportunity

selector-mediated coupling between distant regions

causal sensitivity to experimentally written hidden state,
with trajectory redirection remaining a descriptive interpretation

strong spatial causal containment
```

Those are not fragments left over after failed experiments. They are the positive content of the investigation. They survived because the controls did not remove them, and they arrived increasingly in the substrate's vocabulary rather than biology's.

That changes the question. *Which features of life can we reproduce?* turned out to be an increasingly poor organizing principle for this investigation. Not because the biological questions were useless — they were extraordinarily productive, and they gave us hypotheses sharp enough to fail. But they repeatedly encouraged us to name the phenomenon before discovering what the substrate itself was doing.

The final chapter therefore has to begin from the survivors rather than from the names we hoped to recover. Not *which biological property comes next?* but:

> **What do these computational phenomena add up to?**
