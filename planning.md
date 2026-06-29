Provenance Guard

Project Overview

Provenance Guard is a backend API designed to help creative platforms provide transparent AI attribution for text-based 
content. Rather than making absolute claims about whether a piece of writing is AI-generated, the system combines multiple 
independent detection signals to estimate confidence, communicates that uncertainty to users through understandable 
transparency labels, and provides an appeals workflow for creators who believe their work has been misclassified.

The primary objective is not perfect AI detection—which remains an open research problem—but building a trustworthy 
attribution system that behaves responsibly when evidence is uncertain.

⸻

Problem Statement

As generative AI becomes increasingly capable of producing human-like writing, online platforms face growing challenges 
around attribution and transparency. Writers deserve fair treatment when their work is analyzed, while readers benefit
from understanding when content may have been AI-assisted.

False positives carry significant consequences. Incorrectly labeling original human work as AI-generated can damage a 
creator’s credibility. Because of this, Provenance Guard prioritizes transparent confidence scoring over forcing binary 
decisions.

The system therefore emphasizes:

* Multiple independent detection signals
* Honest uncertainty
* Human review through an appeals process
* Complete auditability of every decision

⸻

System Goals

The system is designed around five engineering goals:

1. Analyze submitted text using multiple independent signals.
2. Combine those signals into a single interpretable confidence score.
3. Present plain-language transparency labels understandable by non-technical users.
4. Allow creators to appeal classifications.
5. Record every decision for accountability and future review.

⸻

Detection Signals

Instead of relying on a single detector, Provenance Guard combines three complementary signals.

Signal 1: LLM Attribution

The primary signal uses Groq’s Llama 3.3 70B model to evaluate whether a passage appears more consistent with AI-generated 
or human-written language.

Output:

* classification
    * likely_ai
    * likely_human
* confidence score between 0 and 1

Strengths

* Understands semantic coherence
* Captures stylistic patterns
* Performs well on longer passages

Limitations

* Cannot guarantee correctness
* Can itself be uncertain
* Sensitive to prompt design

⸻

Signal 2: Stylometric Heuristics

This signal measures structural writing characteristics rather than meaning.

Metrics include:

* vocabulary diversity
* sentence-length variation
* lexical richness

The detector produces an AI-likeness score between 0 and 1.

Strengths

* Fast
* Deterministic
* Does not require external APIs

Limitations

Academic writing, technical documentation, and carefully edited human writing may resemble AI-generated text.

⸻

Signal 3: Repetition Detection

AI-generated text frequently repeats sentence structures, transitions, or vocabulary.

This detector measures:

* repeated words
* repeated phrases
* repetition density

Higher repetition produces a higher AI-likeness score.

Strengths

Simple and inexpensive.

Limitations

Poetry, speeches, lyrics, and intentionally repetitive writing may produce false positives.

⸻

Confidence Scoring

Each detector contributes differently to the final confidence score.

Weights

* LLM Attribution: 70%
* Stylometric Analysis: 20%
* Repetition Analysis: 10%

Final confidence is calculated as a weighted average of all three signals.

The weights were chosen to prioritize semantic analysis from the LLM while allowing stylometric and repetition-based
heuristics to refine borderline cases without dominating the final decision.

⸻

Uncertainty Representation

The confidence score represents the estimated likelihood that a submission exhibits AI-generated characteristics.
Rather than forcing every submission into a binary classification, the system explicitly reserves a range for 
uncertain cases where the detection signals disagree or the evidence is inconclusive.

Classification thresholds

* Likely Human: confidence ≤ 0.35
* Uncertain: 0.35 < confidence < 0.75
* Likely AI: confidence ≥ 0.75

These thresholds intentionally bias the system toward caution. A submission is only labeled as AI-generated 
when multiple signals provide strong supporting evidence. Borderline cases are classified as Uncertain to 
reduce the risk of falsely attributing human-written content to AI.

⸻

Transparency Labels

Three user-facing labels were designed before implementation.

High Confidence AI

“This content is likely AI-generated. Multiple detection signals consistently indicate characteristics commonly
associated with AI-written text.”

⸻

High Confidence Human

“This content is likely human-written. The available evidence suggests the writing reflects characteristics commonly 
found in original human authorship.”

⸻

Uncertain

“Unable to determine confidently. The available evidence is mixed, so we cannot confidently classify this content as 
either AI-generated or human-written. No definitive attribution has been made.”

⸻

Appeals Workflow

Creators may dispute any attribution result.

Each appeal contains:

* content ID
* creator explanation
* review status

Submitting an appeal updates the submission status to:

under_review

The original decision remains preserved in the audit log while the appeal is attached to the same record.

A human reviewer would therefore see:

* original submission
* detection signals
* confidence score
* transparency label
* creator reasoning
* review status

⸻

API Design

POST /submit

Accepts

* creator_id
* text

Returns

* content_id
* attribution
* confidence
* transparency label
* detector scores
* processing timestamp

⸻

POST /appeal

Accepts

* content_id
* creator_reasoning

Updates

* submission status
* appeal information
* audit log

⸻

GET /log

Returns every structured audit entry.

⸻

GET /health

Returns service health.

⸻

Architecture

                 POST /submit
                       │
                       ▼
             Validate Request
                       │
                       ▼
          LLM Attribution Signal
                       │
                       ▼
          Stylometric Analysis
                       │
                       ▼
          Repetition Analysis
                       │
                       ▼
          Confidence Scoring
                       │
                       ▼
        Transparency Label Engine
                       │
                       ▼
              Structured Audit Log
                       │
                       ▼
              JSON API Response
                 POST /appeal
                       │
                       ▼
              Validate Request
                       │
                       ▼
            Update Submission Status
                       │
                       ▼
           Attach Creator Reasoning
                       │
                       ▼
             Update Audit Record
                       │
                       ▼
              JSON Confirmation

Submission Flow

Every submission passes through three independent detectors before being combined into a single confidence score. 
The resulting transparency label is generated from the final confidence, recorded in the audit log, and returned to the client.

Appeal Flow

Appeals never overwrite historical decisions. Instead, the original attribution remains preserved while the appeal 
is attached to the same audit record and marked as under review.

⸻

Anticipated Edge Cases

The system is expected to struggle with several forms of writing.

Formal academic writing

Technical reports often resemble AI due to consistent structure and vocabulary.

Poetry

Heavy repetition and unconventional grammar may confuse heuristic detectors.

Edited AI output

Human editing can remove many stylistic indicators while preserving AI-generated ideas.

Non-native English writing

Simpler sentence construction may appear artificially uniform despite being entirely human-written.

⸻

AI Tool Plan

Milestone 3: Submission Endpoint & First Detection Signal

Context shared with AI: Detection signals, API design, and architecture.

How I used AI: I discussed different ways to structure the Flask application and the submission pipeline, then 
implemented the endpoint and integrated the Groq detector into my design.

Verification: I tested the endpoint with multiple curl requests, validated the JSON responses, and confirmed 
that audit log entries were created correctly before continuing.

⸻

Milestone 4: Multi-Signal Detection & Confidence Scoring

Context shared with AI: Detection signals, confidence-scoring strategy, uncertainty representation, and architecture.

How I used AI: I compared different approaches for combining multiple detection signals, refined the confidence-scoring 
logic, and implemented the stylometric and repetition detectors within the overall pipeline.

Verification: I tested clearly human-written, clearly AI-generated, and borderline examples, inspected each detector
independently, and adjusted the implementation until the confidence scores matched the intended thresholds.

⸻

Milestone 5: Production Layer

Context shared with AI: Transparency labels, appeals workflow, API design, and architecture.

How I used AI: I evaluated different implementations for the transparency labels, appeals workflow, and audit logging 
before integrating them into the existing API.

Verification: I confirmed that all three transparency labels were reachable, verified that appeals updated submissions
to under_review, checked that audit records were updated correctly, and tested rate limiting by triggering HTTP 429 
responses.

⸻

Stretch Features

No stretch features were implemented in this iteration. Development time was prioritized toward producing a complete,
well-documented production pipeline with reliable core functionality before expanding the system further.