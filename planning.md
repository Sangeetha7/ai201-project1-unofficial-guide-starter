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

**Chunk size:** ~500 characters. 

**Overlap:** ~100 characters. This guarantees that explicit keywords (like "Google" or "Cybersecurity Engineer") remain attached to the neighboring sentences.

**Reasoning:** 500 chunk size is large enough to capture an entire interview phase or a multi-sentence technical explanation without bleeding into completely separate comment threads. 100 characters of overlap guarantees that explicit keywords (like "Google" or "Cybersecurity Engineer") remain attached to the neighboring sentences.

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:**  all-MiniLM-L6-v2 via sentence-transformers. It maps text to a 384-dimensional vector space, optimized for semantic sentence similarity while remaining fast and lightweight

**Top-k:** k = 4. Retrieving 4 chunks balances comprehensive coverage without overloading the prompt or introducing off-topic noise.

**Production tradeoff reflection:** In a production system, I would trade this local model for a commercial option (like text-embedding-3-small or a domain-specific Cohere model). This switch would increase the context window capacity, handle complex engineering terminology with greater accuracy, and offer native multilingual support for non-English student posts, though it introduces network API latency and ongoing API costs.

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | What is the reported application timeline for the Amazon SDE Intern position for Summer 2026? | Applied in August/September, completed Online Assessment (OA) within days, final interviews wrapped up by October/November. |
| 2 | What specific technical topics or coding questions were asked during the Google SWE Intern interview? | LRU cache implementation and graph/shortest-path matrix problems. |
| 3 | What are the core technical concepts a candidate must study for a SOC Analyst Tier 1 interview? | OSI model layers, common ports (e.g., 80, 443, 22), the difference between TCP and UDP, and basic phishing indicator triage. |
| 4 | How does Adobe structure its SWE internship interview process? | An initial resume screen, an online technical assessment, followed by consecutive rounds of technical and architectural live interviews.|
| 5 | What scenario-based questions are commonly used to evaluate junior cybersecurity entry-level applicants?| Responding to a hypothetical alert showing a high volume of outbound traffic over an unusual port, or handling an employee clicking a suspected phishing link.|

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1. Social media data is heavily fragmented. If a chunk contains the sentence "The technical round was brutal, they asked two graph questions," but the company name or role title was only mentioned 1,000 characters earlier in the post, the retrieved chunk will be completely contextless.

2. Interview styles change drastically by year. A chunk discussing a 2023 interview process might contradict a 2026 timeline. The retrieval system must avoid mixing obsolete processes with current ones unless explicitly requested.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

[Document Ingestion]      --> Read local markdown or raw text scraped from your 10 URLs
         ↓
 [Text Chunking]          --> Fixed Character Splitter (Size: 500, Overlap: 100) using LangChain
         ↓
[Vector Database]         --> Embed chunks via 'all-MiniLM-L6-v2' -> Store in ChromaDB
         ↓
 [Query Retrieval]        --> Vector semantic similarity search fetches top k=4 chunks
         ↓
 [LLM Generation]         --> Context chunks + System Grounding Prompt fed to LLM -> Final Response
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

**Milestone 3 — Ingestion and chunking:** I will feed my Chunking Strategy section to the AI tool and request a Python script utilizing langchain.text_splitter.CharacterTextSplitter. I will verify that the final chunk count is accurate and inspect boundaries manually to ensure sentences are not cut in half arbitrarily

**Milestone 4 — Embedding and retrieval:** I will provide the Retrieval Approach section to the AI to construct the ChromaDB collection integration using sentence-transformers. I will verify the output by printing the similarity scores of the top-4 chunks for Test Question #3.

**Milestone 5 — Generation and interface:** I will provide my complete Anticipated Challenges and Evaluation Plan to the AI to write the final inference loop, enforcing strict system prompts that prevent hallucination outside the retrieved text.
