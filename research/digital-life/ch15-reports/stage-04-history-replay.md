# Stage 4 — Can the Past Be Reconstructed?

Two different notions of replay were tested.

### Procedural replay

Start from the original seed and replay the same input through the same frozen
rule.

- Exact final morphology: **True**
- Exact final process state: **True**

### Event-log replay

Ignore stochastic re-execution and instead replay the recorded cell-addition
events.

- Exact final morphology: **True**
- All trajectory hashes match: **True**
- Matching trajectory hashes: **96/96**

Figure: `static\images\books\digital-life\ch15-04-history-replay.png`

The event log is a genuine formation record only if it can reconstruct every
recorded state, not merely something visually similar.
