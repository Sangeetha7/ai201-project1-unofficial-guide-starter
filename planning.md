# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? -->

This Unofficial Guide aggregates real student experiences, application timelines, and specific technical questions for entry-level Software Engineering and Cybersecurity internships. This knowledge is traditionally hard to find because it is scattered across transient social media threads and forums, making it difficult for students to accurately gauge how long a company's hiring process takes or what specific concepts to study for the technical rounds.


---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | Reddit (r/csMajors) | Amazon SDE Intern Summer 2026 Application Timeline | https://www.reddit.com/r/csMajors/comments/1sybrw8/amazon_sde_intern_summer_2026_timeline_applied_in/ |
| 2 | Reddit (r/csMajors) | Google SWE Intern Application Timeline | https://www.reddit.com/r/csMajors/comments/1r0oqwb/google_swe_intern_application_timeline/ |
| 3 | Reddit (r/csMajors) | Google Software Engineering Intern Technical Interview | https://www.reddit.com/r/csMajors/comments/1ogk7mg/google_software_engineering_intern_ms_summer_2026/ |
| 4 | Reddit (r/csMajors) | Adobe SWE Intern Interview Process 2026 | https://www.reddit.com/r/csMajors/comments/1qi8txr/adobe_swe_intern_interview_process_2026/ |
| 5 | Reddit (r/csMajors) | Timeline for HPE SWE Intern 2026 | https://www.reddit.com/r/csMajors/comments/1s2rl7u/timeline_for_hpe_swe_intern_2026/ |
| 6 | Reddit (r/cybersecurity) | SOC Analyst Tier 1 Interview Experience & Questions | https://www.reddit.com/r/cybersecurity/comments/1jbui2y/soc_analyst_tier_1_interview/ |
| 7 | Reddit (r/cybersecurity) | Best Cybersecurity Interview Questions Thread | https://www.reddit.com/r/cybersecurity/comments/1ro0c6l/what_were_some_of_the_best_interview_questions/ |
| 8 | Reddit (r/cybersecurity) | Junior Cyber Security Analyst Interview Breakdown | https://www.reddit.com/r/cybersecurity/comments/14yj019/junior_cyber_security_analyst_interview/ |
| 9 | Reddit (r/cybersecurity) | Technical Questions for Cybersecurity Engineers | https://www.reddit.com/r/cybersecurity/comments/1pilmec/what_technical_questions_do_you_use_when/ |
| 10 | Reddit (r/cybersecurity) | Open-Ended and Scenario-Based Interview Questions | https://www.reddit.com/r/cybersecurity/comments/1554itn/what_are_some_openended_scenariobased_interview/ |

---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:**

**Overlap:**

**Reasoning:**

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:**

**Top-k:**

**Production tradeoff reflection:**

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | | |
| 2 | | |
| 3 | | |
| 4 | | |
| 5 | | |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1.

2.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

---

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->

**Milestone 3 — Ingestion and chunking:**

**Milestone 4 — Embedding and retrieval:**

**Milestone 5 — Generation and interface:**
