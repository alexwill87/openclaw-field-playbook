# QUALITY.md — Editorial Quality Protocol
## The OpenClaw Field Playbook

> **This document is agent-ready.**  
> An AI agent can execute all checks autonomously and produce a scored report.  
> Output: a dated entry appended to `_project/SECTIONS-SCORES.md`.

---

## How to use this document

**If you are an AI agent:**
1. Read this entire document before starting any check
2. For each section to audit: receive the file path as input
3. Execute all checks in each dimension in order
4. Assign a score 1-5 per dimension (see scoring scale below)
5. Output a structured report using the template at the end of this document
6. Append the result to `_project/SECTIONS-SCORES.md`

**If you are a human maintainer:**
- Use this as a review checklist before approving any PR that changes a section
- A section needs an average score ≥ 3/5 across all dimensions to move to `status: review`
- A section needs an average score ≥ 4/5 to move to `status: complete`

---

## Scoring scale

```
1 — Absent or non-functional
    The criterion is completely missing or the section cannot be used as written.

2 — Present but insufficient
    The criterion exists but fails on multiple sub-checks.
    Usable only with significant modification.

3 — Acceptable
    The criterion is met on most sub-checks.
    Usable with minor adjustments.

4 — Good
    The criterion is fully met.
    Ready to publish with no required changes.

5 — Reference quality
    Exceeds the criterion. Sets the standard for this type of content.
    Can be used as an example for future contributors.
```

---

# DIMENSION 1 — Scientific rigour

*Does the section say only what it can support?*

## D1-01 — Experience vs opinion distinction

**What to check:**
Read every claim in the section. Identify claims that are not based on documented experience or a verifiable source.

**Process:**
1. Extract all declarative statements ("X works", "Y is better than Z", "Always do W")
2. For each: is it labelled as personal experience, community observation, or general recommendation?
3. Flag any absolute claim ("always", "never", "best") that has no basis

**PASS criteria:**
- Every claim is either: grounded in stated experience, attributed to a source, or explicitly labelled as a recommendation
- Speculative content is clearly marked ("In our experience...", "This may vary...")

**FAIL criteria:**
- Unqualified absolute statements ("OpenClaw always handles X better than Y")
- Opinions presented as facts without labelling

**Action if FAIL:**
Add qualifiers to absolute statements. Prefix speculative content with "In practice..." or "Based on [context]..."

---

## D1-02 — Limits explicitly stated

**What to check:**
Does the section tell the reader when this content does NOT apply?

**Process:**
1. Read the Context block
2. Check if there is a statement about scope limits (who this is NOT for, what context this does NOT cover)
3. Check Common mistakes for cases where the advice fails

**PASS criteria:**
- At least one explicit statement of scope limits
- Common mistakes section addresses failure cases, not just user errors

**FAIL criteria:**
- Section presents universal advice that is actually context-specific
- No mention of cases where the approach breaks

**Action if FAIL:**
Add a "This does not apply when..." statement to the Context block.

---

## D1-03 — Technical claims verifiable

**What to check:**
Any technical claim (configuration syntax, API behaviour, tool capability) must be verifiable.

**Process:**
1. Extract all technical statements
2. Check if they can be verified by following the step-by-step
3. Identify claims that depend on a specific version or context without stating it

**PASS criteria:**
- Technical steps are reproducible as written
- Version-dependent information states the version

**FAIL criteria:**
- Steps reference features that may not exist in all versions
- Configuration examples use syntax that cannot be verified from the section alone

**Action if FAIL:**
Add version context. Add a note: "Verified with OpenClaw [version] as of [date]."

---

# DIMENSION 2 — Exhaustiveness

*Does the section cover what its title promises?*

## D2-01 — Title-content alignment

**What to check:**
Read the section title. Then read the section. Does the content fully deliver on the title's promise?

**Process:**
1. Extract the key noun(s) from the title
2. Check that each key concept is addressed in the body
3. Identify topics the title implies but the section skips

**PASS criteria:**
- Every concept implied by the title has at least one substantive paragraph
- No major gap between the promise and the delivery

**FAIL criteria:**
- Title says "Installing OpenClaw on a cloud server" but only covers local installation
- Key concept is mentioned but not explained

**Action if FAIL:**
Either expand the section to cover missing concepts, or narrow the title to match actual content.

---

## D2-02 — Edge cases addressed

**What to check:**
Does the section acknowledge what happens when things go wrong or when the reader's context differs?

**Process:**
1. Read Common mistakes
2. Check if the most predictable failure scenarios are listed
3. Check if the section acknowledges context variations (team vs solo, FR vs EN environment, etc.)

**PASS criteria:**
- At least 2 common mistakes documented
- At least 1 context variation acknowledged

**FAIL criteria:**
- Common mistakes section is empty or contains only trivial points
- Section assumes a single context without acknowledging alternatives

**Action if FAIL:**
Add 1-2 realistic failure scenarios based on the content of the section.

---

## D2-03 — Template coverage

**What to check:**
Does the Template block cover the main use case described in the section?

**Process:**
1. Identify the primary use case described in Step-by-step
2. Check that the Template directly supports that use case
3. Check that the Template is not a generic placeholder

**PASS criteria:**
- Template directly applies to the section's primary use case
- Template is specific enough to be useful without reading the full section

**FAIL criteria:**
- Template is a generic "fill in your details" block with no section-specific content
- Template covers a different use case than the section body

**Action if FAIL:**
Rewrite Template to reflect the specific configuration or prompt described in the section.

---

# DIMENSION 3 — Editorial form

*Is the section written to the playbook's standards?*

## D3-01 — Standard format respected

**What to check:**
Does the section contain all required blocks in the correct order?

**Required blocks in order:**
```
1. Metadata block (YAML front matter)
2. Section title (H2)
3. Who this is for / Time required / Difficulty
4. ### Context
5. ### Step-by-step
6. ### Common mistakes
7. ### 🌍 Local specifications
8. ### Template
```

**Process:**
Check for presence and order of each block.

**PASS criteria:** All 8 blocks present in order.
**WARN criteria:** All blocks present but in different order.
**FAIL criteria:** One or more blocks missing entirely.

**Action if FAIL:**
Add missing blocks. Use placeholder text if content is not yet available.

---

## D3-02 — No filler content

**What to check:**
Does every sentence add information the reader needs?

**Process:**
1. Read each paragraph
2. Flag sentences that restate what was already said
3. Flag sentences that are generic ("AI is changing the world", "This is important")
4. Count filler phrases: "It is worth noting that", "As mentioned above", "In conclusion"

**PASS criteria:**
- Zero or one filler phrase per section
- No paragraph that repeats information from another paragraph

**FAIL criteria:**
- Three or more filler phrases
- Opening paragraph is purely contextual with no actionable information

**Action if FAIL:**
Delete filler sentences. Start the Context block with the problem, not the background.

---

## D3-03 — Metadata block complete and accurate

**What to check:**
Does the YAML front matter contain all required keys with valid values?

**Required keys and valid values:**
```yaml
status: draft | review | complete
audience: human | agent | both
chapter: 00 | 01 | 02 | 03 | 04 | 05 | 06 | 07
last_updated: YYYY-MM
contributors: [list — empty list [] is acceptable]
```

**PASS criteria:** All 5 keys present with valid values.
**FAIL criteria:** Any key missing or invalid value.

**Action if FAIL:**
Add or correct the metadata block.

---

## D3-04 — Template is copy-paste ready

**What to check:**
Can the Template block be copied and used without structural modification?

**Process:**
1. Copy the template as written
2. Identify bracketed fields: `[your name]`, `[context]`, etc.
3. Check if bracketed fields are clear enough to fill in without reading the section
4. Check if the template format matches what OpenClaw actually accepts

**PASS criteria:**
- All bracketed fields are self-explanatory
- Template is in a code block with correct syntax highlighting
- No mandatory reading required before using the template

**FAIL criteria:**
- Bracketed fields are ambiguous (`[add your thing here]`)
- Template requires understanding the full section to use

**Action if FAIL:**
Add inline comments to explain each bracketed field. Example: `[your business name — e.g. "Dupont Consulting"]`

---

# DIMENSION 4 — Human readability

*Can a non-technical entrepreneur apply this section without help?*

## D4-01 — Jargon explained at first use

**What to check:**
Every technical term used for the first time must be explained or linked to the Glossary.

**Process:**
1. List all technical terms (agent, trigger, memory, token, webhook, etc.)
2. Check if each term is explained within the section or linked to Chapter 1 Glossary
3. Flag unexplained jargon

**PASS criteria:**
- No unexplained technical term
- Glossary link used for terms defined there

**FAIL criteria:**
- Technical terms used without explanation and no Glossary link

**Action if FAIL:**
Add a one-line explanation in parentheses at first use, or link to Glossary.

---

## D4-02 — Difficulty level accurate

**What to check:**
Does the stated difficulty (Beginner / Intermediate / Advanced) match the actual content?

**Process:**
1. Read the declared difficulty level
2. Assess the actual complexity: prerequisites required, number of steps, technical depth
3. Evaluate mismatch

**PASS criteria:** Declared difficulty matches content within one level.
**FAIL criteria:** Declared Beginner but content requires technical prerequisites.

**Action if FAIL:**
Adjust the difficulty declaration, or add a "Prerequisites" note.

---

## D4-03 — Steps are executable in order

**What to check:**
Can a reader follow Step-by-step from top to bottom without needing external information?

**Process:**
1. Read Step-by-step as if executing it for the first time
2. Identify steps that assume knowledge not provided earlier in the section
3. Identify steps where the expected result is not stated

**PASS criteria:**
- Each step states what to do AND what the result should be
- No step requires knowledge from outside the section

**FAIL criteria:**
- Step says "configure X" without explaining how
- Expected result not stated (reader cannot verify success)

**Action if FAIL:**
Add "Expected result:" after each non-trivial step.

---

# DIMENSION 5 — Agent readability

*Can an AI agent parse and act on this section without ambiguity?*

## D5-01 — Instructions are unambiguous

**What to check:**
Can every instruction be executed by an agent without interpretation?

**Process:**
1. Extract every imperative sentence ("Do X", "Set Y to Z", "Configure W")
2. Check if each has a clear, deterministic outcome
3. Flag instructions with multiple valid interpretations

**PASS criteria:**
- Every instruction has one clear execution path
- No instruction requires judgment without defined criteria

**FAIL criteria:**
- Instructions like "adjust as needed" or "configure appropriately" without criteria

**Action if FAIL:**
Replace vague instructions with specific criteria. "Adjust as needed" → "If [condition], use [value A]. Otherwise, use [value B]."

---

## D5-02 — Template is parseable

**What to check:**
Can an agent extract and apply the Template block programmatically?

**Process:**
1. Check that the Template is in a properly closed code block
2. Check that bracketed fields follow a consistent format: `[descriptor]` or `[descriptor — example]`
3. Check that there are no nested code blocks

**PASS criteria:**
- Template is in a single, properly closed code block
- All variable fields use consistent bracket notation
- No formatting that would break programmatic extraction

**FAIL criteria:**
- Template uses mixed notation (`[field]`, `{field}`, `<field>`)
- Code block is not closed
- Template contains explanatory prose mixed with the prompt/config

**Action if FAIL:**
Standardise bracket notation. Move explanatory prose outside the code block.

---

## D5-03 — Metadata parseable

**What to check:**
Is the YAML front matter valid and parseable?

**Process:**
Attempt to parse the front matter as YAML. Check for:
- Consistent indentation
- No unquoted special characters
- Valid values for all keys

**PASS criteria:** Front matter parses without errors.
**FAIL criteria:** Any YAML parsing error.

**Action if FAIL:**
Correct the YAML syntax. Quote strings containing special characters.

---

# DIMENSION 6 — Bilingual coherence

*Is the section correctly structured for both EN and local contexts?*

## D6-01 — Local specifications block present

**What to check:**
Does the section contain the `## 🌍 Local specifications` block?

**Process:**
Search for the exact heading `## 🌍 Local specifications`.

**PASS criteria:** Block present.
**WARN criteria:** Block present but contains only `*[See sections/07-localisation/...]*`
**FAIL criteria:** Block absent entirely.

**Action if FAIL:**
Add block with placeholder: `*[See sections/07-localisation/ for local adaptations]*`

---

## D6-02 — fr-FR localisation entry exists

**What to check:**
For each `status: complete` section, does a corresponding entry exist in `sections/07-localisation/fr-FR.md`?

**Process:**
1. Check the section's `status` in its metadata block
2. If `status: complete`: check `07-localisation/fr-FR.md` for a section referencing this content
3. If `status: draft` or `review`: this check is WARN, not FAIL

**PASS criteria:** Entry exists in fr-FR.md for complete sections.
**WARN criteria:** Section is draft/review — localisation not yet required.
**FAIL criteria:** Section is complete but no fr-FR entry exists.

**Action if FAIL:**
Create localisation entry in `07-localisation/fr-FR.md` or downgrade section status to `review`.

---

## D6-03 — Technical terms not translated in local specs

**What to check:**
In `07-localisation/fr-FR.md` and any locale file, technical terms (YAML keys, file names, labels) must remain in English.

**Process:**
Read the locale file. Check that these terms are not translated:
- YAML keys: `status`, `audience`, `chapter`
- GitHub labels: `suggestion`, `correction`, `governance`
- File names referenced
- Command-line instructions

**PASS criteria:** All technical terms in English in locale files.
**FAIL criteria:** Any technical term translated in a locale file.

**Action if FAIL:**
Revert translated technical terms. Add a note explaining the language contract.

---

# Quality Report Template

After running all checks, output a report using this exact format:

```markdown
# Quality Report — [YYYY-MM-DD]
## Section: [file path]
## Audited by: [agent name or "manual"]

### Scores

| Dimension | Score (1-5) | Key issues |
|-----------|-------------|------------|
| D1 — Scientific rigour | [score] | [summary or "none"] |
| D2 — Exhaustiveness | [score] | [summary or "none"] |
| D3 — Editorial form | [score] | [summary or "none"] |
| D4 — Human readability | [score] | [summary or "none"] |
| D5 — Agent readability | [score] | [summary or "none"] |
| D6 — Bilingual coherence | [score] | [summary or "none"] |
| **Average** | **[avg]** | |

### Status recommendation
- Current status: [draft | review | complete]
- Recommended status: [draft | review | complete]
- Reasoning: [one sentence]

### Failed checks
[List each FAIL with dimension, check ID, and corrective action]
[If none: "No failed checks."]

### Warnings
[List each WARN with dimension, check ID, and note]
[If none: "No warnings."]

### Priority actions
1. [Most critical — with specific file and line if possible]
2. [Second priority]
3. [Third priority]
[Stop at 5 actions maximum]
```

---

*Append completed reports to `_project/SECTIONS-SCORES.md`.*
