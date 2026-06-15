# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

<!-- What topic or category of knowledge does your system cover?
     Why is this knowledge valuable, and why is it hard to find through official channels?
     Example: "Student reviews of CS professors at [university] — useful because official
     course descriptions don't reflect teaching style, exam difficulty, or workload." -->

---

This Unofficial Guide aggregates real student experiences, application timelines, and specific technical questions for entry-level Software Engineering and Cybersecurity internships. This knowledge is traditionally hard to find because it is scattered across transient social media threads and forums, making it difficult for students to accurately gauge how long a company's hiring process takes or what specific concepts to study for the technical rounds.


## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

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

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:** 700 characters

**Overlap:** 150 characters

**Why these choices fit your documents:** Reddit posts and forum threads include short, noisy lines (upvote text, handles, ads) that fragment meaning when using small fixed chunks. A 700-character chunk gives each embedding more contextual scope to capture semantic intent across sentence boundaries, while a 150-character overlap preserves continuity so that important phrases split across boundaries remain retrievable. Preprocessing removes UI noise, normalizes whitespace, and strips metadata before chunking to ensure chunks are content-focused.
pipeline.
**Final chunk count:** 138
 
---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:** text-embedding-3-small — a compact, cost-efficient embedding model with good general-purpose semantic accuracy suitable for short forum posts and mixed-format text; choose a larger embedding model if higher semantic fidelity is required.

**Production tradeoff reflection:** For production I would weigh accuracy vs cost and latency: larger models give better retrieval precision but increase API cost and response time. Consider hosting a smaller model locally (e.g., MiniLM) for privacy and lower per-query cost, or use a larger cloud model when accuracy and multilingual support matter. Also tune re-index frequency and chunking to balance freshness, compute cost, and retrieval quality.

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:** Use only the provided retrieved document context when answering. Do not hallucinate or add facts not present in the sources; if the answer cannot be found in the provided documents, reply “I don’t know based on the documents” and offer follow-up options. For any factual claim, include an inline source citation (bracketed) and a short quoted excerpt when helpful. Keep answers concise, and avoid disallowed content and speculative reasoning.

**How source attribution is surfaced in the response:**
 Inline citations: bracketed tags after claims (e.g., [source: source_2.txt]).
Footer "Sources": list each cited file/chunk with a one-line excerpt and the retrieval similarity score.
If no source supports the claim, state that explicitly and do not provide attribution.
---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | What is the reported application timeline for the Amazon SDE Intern position for Summer 2026? | Applied in August/September, completed Online Assessment (OA) within days, final interviews wrapped up by October/November. | Applied Oct 2025; online assessment received Mar 2, 2026 and completed Mar 3; interview invite Mar 24; final interviews Apr 9; offer extended Apr 15, 2026 — ~6 months from application to offer.|  relevant | accurate
| 2 | What specific technical topics or coding questions were asked during the Google SWE Intern interview? | LRU cache implementation and graph/shortest-path matrix problems. | I don't have enough information on that based on the provided documents. | off-target | inaccurate
| 3 | What are the core technical concepts a candidate must study for a SOC Analyst Tier 1 interview? | OSI model layers, common ports (e.g., 80, 443, 22), the difference between TCP and UDP, and basic phishing indicator triage. | EDR and SIEM tooling (queries), networking/security fundamentals (ports, OSI, CIA, TCP/UDP), Active Directory attacks/mitigations, virtualization platforms, perimeter/security tech (WAF/proxy/IDS/IPS/firewall), basic malware analysis, familiarity with Splunk/QRadar, plus strong scenario-based problem‑solving. | relevant | accurate
| 4 | How does Adobe structure its SWE internship interview process? | An initial resume screen, an online technical assessment, followed by consecutive rounds of technical and architectural live interviews.| I don't have enough information on that based on the provided documents. The text only mentions some aspects of the interview process, such as a virtual interview, a HackerRank test, and a technical interview, but it does not provide a comprehensive overview of the structure of the SWE internship interview process. | off-target | inaccurate
| 5 | What scenario-based questions are commonly used to evaluate junior cybersecurity entry-level applicants?| Responding to a hypothetical alert showing a high volume of outbound traffic over an unusual port, or handling an employee clicking a suspected phishing link.| I don't have enough information on that based on the provided documents. The documents mention that scenario-based questions will be asked, but they do not provide specific examples of the questions. They only mention that the questions will be "open-ended, scenario-based questions" for an entry-level SOC analyst position, and that the interviewer may ask questions across different areas such as EDR, MFA, firewalls, incident response, OSI, and NIST CSF, but no specific scenario-based questions are provided. | off-target | inaccurate



**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:** specific technical topics or coding questions asked during the Google SWE Intern interview

**What the system returned:** the system returned a distance score of 0.90+ and substituted Adobe SWE questions instead

**Root cause (tied to a specific pipeline stage):** This occurred because source_2.txt contained an explicit statement that the author signed an NDA and could not share technical details.

**What you would change to fix it:** Because the target information did not exist in the source dataset, the semantic embedding model mapped the query to the closest available technical interview text (Adobe), and the LLM correctly refused to hallucinate Google data due to our strict grounding system prompt.

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**

The spec clarified measurable goals (chunking, overlap, grounding, and evaluation questions) which made design decisions straightforward and testable. Having explicit test questions and success criteria from planning.md kept development focused on retrieval quality and guided iterative tuning of chunk sizes and prompt instructions.

**One way your implementation diverged from the spec, and why:**

I increased the chunk size and overlap (from the originally planned 500/100 to 700/150) and made chunking parameters dynamic to cope with noisy Reddit-formatted text and improve retrieval relevance. I also moved the parameter handling out of the test loop into ingest.py to avoid mismatches and added defensive checks for missing metadata—practical adjustments driven by real data and a runtime crash during testing.
---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

- *What I gave the AI:* A description of conversational Reddit UI noise (upvote text, promoted ads, user handles) and an instruction to change chunking from 500 characters to 700 characters with 150-character overlap, applied dynamically in the ingestion pipeline.
- *What it produced:* Suggested pipeline updates to use 700-character chunks with 150 overlap and to make chunking parameters configurable rather than hardcoded.
- *What I changed or overrode:* Confirmed and enforced the final parameters (700 / 150) and ensured the pipeline applies them dynamically at runtime.

**Instance 2**

- *What I gave the AI:*  A bug report: the test script was hardcoding chunking parameters inside its execution loop (bypassing changes in ingest.py) which caused a NoneType metadata crash; request to rewrite the script to accept parameters dynamically and to handle empty or missing dictionary metadata safely.
- *What it produced:* A rewritten test script design that passes chunking parameters dynamically from the ingestion code and includes guards for empty/missing metadata structures.
- *What I changed or overrode:* Removed the hardcoded parameters in the test script, validated dynamic parameter passing from ingest.py, and added safe checks to prevent the NoneType metadata crash.
