# Stage 2 — Save, Restore, Continue

The midpoint state was serialized to SQLite, loaded into a new runtime state,
and continued using the remaining input.

Results:

- Exact final morphology: **True**
- Exact final process state: **True**
- Population trajectory identical: **True**
- Attachment trajectory identical: **True**
- Symmetric-difference cells: **0**

Reference morphology hash: `bc8e6d8c9783431f1459bf17`  
Restored morphology hash: `bc8e6d8c9783431f1459bf17`

Reference process hash: `bd33c9aa0a510803be6ce6bf`  
Restored process hash: `bd33c9aa0a510803be6ce6bf`

Figure: `static\images\books\digital-life\ch15-02-exact-restore.png`

An exact pass means the checkpoint preserved sufficient process state to resume
the stochastic growth process without changing its future.
