---
status: complete
audience: both
chapter: 01
last_updated: 2026-04
contributors: [alexwill87, claude-cockpit]
lang: en
---

# 1.2 -- The distinction between proactive vs reactive

**Who this section is for:** Any user who wants to understand what makes the difference between an assistant that waits and an assistant that moves forward.
**Reading time:** 10 minutes.
**Difficulty:** Beginner.

### Context

Most AI tools you use today are reactive. You ask a question, they answer. You give an instruction, they execute. Then they wait. In silence.

It's useful, but it's the first level. And the majority of users stay stuck at this level.

### Dennis Steinberg's spiral

Dennis Steinberg formalized a four-stage progression to describe what an AI agent should be able to do:

```
Understand -> Automate -> Decide -> Reflect
     |                                 |
     +<-------------------------------+
```

**Understand:** The agent can interpret your context. It doesn't respond in a vacuum -- it knows who you are, what you do, what your tools are, your constraints.

**Automate:** The agent executes repetitive tasks without intervention. No need to ask it every time: it knows that Monday morning, it needs to prepare the weekly briefing.

**Decide:** The agent makes choices within a framework you've defined. "If stock falls below X, place the order. If the client hasn't responded in 48 hours, follow up." It doesn't ask you for approval on every micro-decision.

**Reflect:** The agent evaluates its own results. Did what it did produce the expected outcome? Should we adjust? This is the feedback loop that transforms an automaton into an adaptive system.

The return arrow is crucial. It's not a linear progression -- it's a spiral. Each cycle enriches understanding, which enriches automation, and so on.

### What this changes in practice

An agent that only understands (level 1) is a glorified ChatGPT. It's useful, but it doesn't save you time in a structural way.

An agent that understands and automates (levels 1-2) starts to create real value. Repetitive tasks disappear from your day.

An agent that understands, automates, and decides (levels 1-3) changes how you work. You no longer manage the details -- you define the rules and validate the results.

An agent that cycles through all four levels is a system that improves over time. That's what OpenClaw is designed to bring you toward.

> **Principle:** An agent that waits for your questions only serves 20% of its potential. Real value begins when it acts on its own, within a framework you've defined.

> **Field note:** In practice, most OpenClaw installations start at levels 1-2. That's normal. Level 3 requires trust in the system, and trust builds over time. Don't skip steps -- an agent that decides too early without a clear framework is a problem, not a solution.
