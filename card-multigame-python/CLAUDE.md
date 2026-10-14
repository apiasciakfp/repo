## GENERAL IMPLEMENTATION

- Every nontrivial plan should get a Devil's Advocate (Adversarial Agent) pass.
- Every implementation should get appropriate automated tests capturing **business intentions** not **implementation**.
- If you are not sure about user's intentions, do not assume - ask the user.

## SPECIALIZED SUBAGENTS

### Devil's Advocate Subagent

**Purpose**: Challenge assumptions before commitment

**Triggers**:
- After Orient phase (before Decide)
- After plan is drafted (before approval)
- When user or Claude proposes a decision

**Behavior**:
- Spawn subagent with prompt: "Argue against this approach. What assumptions might be wrong? What could fail? What are we not seeing?"
- Subagent returns challenges
- Overseer documents in `XX-claude-devils-advocate-[topic].md`
- Proceed only after challenges are addressed or acknowledged

**Target**: Sometimes against CC's analysis, sometimes against user's direction. The goal is finding blind spots, not winning arguments.

### Verification Subagent

**Purpose**: Confirm implementation meets acceptance criteria

**Triggers**:
- Before marking any phase complete
- Before `COMPLETE-` prefix is added to any document

**Behavior**:
- Spawn subagent with: "Verify this implementation against acceptance criteria. Does it actually work? Run tests. Check manually. Report gaps."
- Subagent performs independent verification
- Phase not complete until verification passes

**Rule**: Implementation is not "done" because code was written. It's done when verification confirms it works.

## PROVABLE VERTICAL SLICES

The training manual (Part 5) requires provable units of work — observable reality changed, demonstrated at the fidelity the claim demands. This section defines HOW to prove them in code. **Slice size follows provability need**: a slice can be large if honest proof requires it — what's fixed is "standalone + provable", never "small". Order by risk retired (see Risk-First Slice Ordering below).

### Every slice MUST specify

```markdown
## Slice: [Name]

### Contract
- Input type: [typed record/schema]
- Output type: [typed record/schema]
- Preconditions: [what must be true before calling]
- Postconditions: [what is guaranteed after calling]
- Invariants: [what never changes]

### Verification
- Properties: [universal truths — round-trip, idempotency, commutativity, domain rules]
- Happy path: [one concrete example test]
- Failure case: [one explicit error path]
- Method: [property-based | invariant-example | concrete-example | manual | type-check-only]

### Deletion boundary
- Depends on: [list of other slices this uses]
- Depended on by: [list of slices that use this]
- Can delete independently: [yes/no — if no, explain why]
```

The deletion boundary IS the connascence graph: `depends-on` / `depended-on-by` are the locality and degree of the slice's coupling. A slice that can't be deleted independently is a slice with high cross-boundary connascence — flag it.

### Property patterns to look for

- **Round-trip**: `deserialize(serialize(x)) == x`
- **Idempotency**: `f(f(x)) == f(x)`
- **Invariant preservation**: `len(pool_after_draw) == len(pool_before) - 1`
- **Commutativity**: `merge(a, b) == merge(b, a)`
- **Domain constraints**: `all tokens in result are subset of input pool`
- **No-op on empty**: `f([]) == []`

## DEVIATION CAPTURE TOOL

### DEVIATION - Corrective document

**DEVIATION** — a principle-level correction (I did X, you wanted Y). After sufficiently important deviations → extract a DEVIATION document.

### When the user corrects you

1. **Acknowledge by acting** — apply the correction immediately. Do *not* say "you're right" or scripted apologies; acknowledgment is implicit in acting on it. State your *corrected understanding*, not contrition.
2. **Recognise it as a DEVIATION** if it's principle-level (not a one-off fact) — announce: "I think we have a DEVIATION here; let me state what I'm understanding before we capture it."
3. **Present for review BEFORE filing** — a wrong DEVIATION is worse than none:
   - **LEVEL** — PRINCIPLE (always true) or TACTICAL (context-specific — listen for "since this is a prototype…", "because we need to ship…")
   - **WHAT HAPPENED** — I wanted to [X]; you corrected me to [Y — exact quote]
   - **THE DEEP WHY** — I believed [my worldview]; you believe [your worldview]
   - **THE PRINCIPLE/RULE** — one-sentence capture
   - **WHEN IT APPLIES** — always (PRINCIPLE) or [specific context] (TACTICAL)
   - "Is this right? What am I missing?"
4. **Refine until the user confirms** ("Perfect!" / equivalent). Only then create `XX-DEVIATION-[topic].md`.
5. **Extract a PATTERN** after 3 similar DEVIATIONs. Cross-domain PATTERNs/DEVIATIONs are promotion candidates — sub-`CLAUDE.md`, memory, this manual.
