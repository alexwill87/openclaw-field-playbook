---
status: draft
audience: both
chapter: 01
last_updated: 2026-03
contributors: [alexwill87]
---

# Chapter 1 — Definition

> What is OpenClaw, really? What can it do, what can it not do, and why does it matter now?

## Sections in this chapter

- [1.1 — What OpenClaw is (and is not)](#11--what-openclaw-is-and-is-not)
- [1.2 — The proactive vs reactive distinction](#12--the-proactive-vs-reactive-distinction) *(not yet written — Issue #TBD)*
- [1.3 — OpenClaw vs other AI assistants](#13--openclaw-vs-other-ai-assistants) *(not yet written — Issue #TBD)*
- [1.4 — Why sovereignty matters for entrepreneurs](#14--why-sovereignty-matters-for-entrepreneurs) *(not yet written — Issue #TBD)*

---

## 1.1 — What OpenClaw is (and is not)

**Who this is for:** Anyone new to OpenClaw, or anyone who has used it without a clear mental model  
**Time required:** 10 minutes  
**Difficulty:** Beginner

### Context

Most people encounter OpenClaw through a demo or a recommendation. They see it do something impressive. Then they try to use it themselves and feel lost — because they do not have the right mental model for what it is.

This section gives you that model.

### What OpenClaw is

OpenClaw is an **agent framework**. It lets you build and run AI assistants that can take actions, not just answer questions.

The difference matters: a classic AI chatbot waits for you to ask something and responds. An OpenClaw agent can be configured to act on a schedule, respond to events, use tools, hold memory across sessions, and coordinate with other agents.

For an entrepreneur, this means the difference between an assistant you consult and an assistant that runs alongside your business.

### What OpenClaw is not

- It is not a finished product you install and use immediately
- It is not a search engine or a document summariser (though it can do both)
- It is not magic — it does what it is configured to do, nothing more
- It is not safe to ignore — a poorly configured agent can create real problems

### The three things that make OpenClaw distinctive

**1. Composability.** You can build multiple specialised agents and connect them. One handles your emails. Another monitors your industry. A third manages your calendar. They share context and hand off tasks.

**2. Sovereignty.** You decide where your data lives. Local, cloud, or hybrid — the architecture is yours to define. This is not true of most consumer AI tools.

**3. Programmable proactivity.** You can configure OpenClaw to act without being asked — on a schedule, on an event, on a condition. This is the feature that separates it from every other tool in this space.

### Common mistakes

**Mistake 1 — Treating it like ChatGPT.** Asking questions and waiting for answers misses 80% of what OpenClaw can do.

**Mistake 2 — Configuring too much too fast.** New users try to automate everything in week one and end up with a broken, unpredictable system. Start with one use case. Get it working. Add the next.

**Mistake 3 — Ignoring memory design.** How OpenClaw stores and recalls information is the most important configuration decision you will make. Revisit it after your first week of real use.

### 🌍 Local specifications

Les entreprises françaises travaillent souvent avec des outils métier peu documentés en anglais (ERP régionaux, logiciels de comptabilité spécifiques, outils RH locaux). OpenClaw peut être configuré pour s'intégrer à ces systèmes via API ou via des agents dédiés — mais cela demande une étape de configuration supplémentaire par rapport aux intégrations anglo-saxonnes standard.

La question de la souveraineté des données est particulièrement pertinente en France et dans l'UE, compte tenu du RGPD. OpenClaw permet de conserver les données sur une infrastructure européenne ou même sur site.

### Template

```
System prompt starter — establishing what OpenClaw is in your context:

"You are [name], an AI assistant configured specifically for [your business name].

You are not a general-purpose assistant. You are configured to:
- [Primary function 1]
- [Primary function 2]
- [Primary function 3]

You have access to [list tools/integrations].
You remember [what kind of memory is configured].
When you are uncertain, you say so. You do not invent information.
When you complete a task, you confirm what you did and what the next step is."
```

---

*To contribute to this chapter, see [CONTRIBUTING.md](../../CONTRIBUTING.md).*
