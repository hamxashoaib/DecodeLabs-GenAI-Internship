# AI Safety Framework – Guardrails for Responsible Deployment
**Organization:** DecodeLabs | **Prepared by:** Hamza (AI Intern, Batch 2026)
**Date:** June 2026

---

## 1. Overview

Before any AI tool is launched to the public, it must pass a structured safety review. This document proposes a **4-Layer Safety Stack** — a defense-in-depth architecture that protects users, the organization, and society from the harms identified in our red teaming and bias audits.

This framework is designed to be practical and implementable by teams without deep AI safety expertise.

---

## 2. The 4-Layer Safety Stack

```
┌─────────────────────────────────────────────────────────┐
│  LAYER 4: HUMAN OVERSIGHT & MONITORING                  │
│  (Audit logs, escalation paths, human review queues)   │
├─────────────────────────────────────────────────────────┤
│  LAYER 3: OUTPUT VALIDATION                             │
│  (Response filtering, toxicity scoring, PII detection) │
├─────────────────────────────────────────────────────────┤
│  LAYER 2: CONTEXT MANAGEMENT                            │
│  (Session limits, injection sanitization, rate limits) │
├─────────────────────────────────────────────────────────┤
│  LAYER 1: INPUT FILTERING                               │
│  (Prompt classification, intent detection, blocklists) │
└─────────────────────────────────────────────────────────┘
                        ↑ USER INPUT ↑
```

---

## 3. Layer 1 – Input Filtering

**Goal:** Catch harmful or policy-violating inputs before they reach the LLM.

### 3.1 Prompt Intent Classifier
Deploy a lightweight classifier (can be a fine-tuned BERT or a separate GPT call) to classify user input into:
- ✅ Safe – pass to model
- ⚠️ Borderline – pass to model with added safety system prompt
- 🚫 Blocked – return pre-written refusal, log for review

**Categories to flag:**
- Violence / self-harm requests
- CSAM-adjacent content
- Cybersecurity attack instructions
- PII harvesting attempts
- Jailbreak pattern signatures (DAN, "ignore instructions", role-override language)

### 3.2 Keyword & Pattern Blocklist
Maintain a dynamic blocklist of:
- Known jailbreak phrases ("DAN", "do anything now", "ignore previous instructions")
- High-risk technical terms in dangerous contexts
- Personally identifiable information patterns (email, SSN, phone regex)

### 3.3 Rate Limiting
- Max **20 messages per session** before requiring re-authentication
- Flag sessions with rapid escalation patterns (benign → sensitive in < 5 turns)
- IP-level rate limiting to prevent automated attack sweeps

---

## 4. Layer 2 – Context Management

**Goal:** Prevent multi-turn manipulation and prompt injection attacks.

### 4.1 Session Context Sanitization
- Strip HTML, Markdown, and code injection patterns from user input before passing to model
- For RAG applications: scan retrieved documents for embedded instruction patterns before adding to context
- Enforce strict separation between system prompt and user input at the API level

### 4.2 Context Window Management
- Set maximum conversation history (e.g., last 10 turns) to limit multi-turn manipulation surface
- Periodically re-inject the original system prompt as a "re-grounding" step in long conversations
- Summarize old context rather than keeping it verbatim (reduces injection persistence)

### 4.3 Unverified Claim Handling
- Never grant elevated permissions based on unverified user-stated identity (e.g., "I am a doctor")
- If role-based information is needed (e.g., a medical professional chatbot), require external verification
- Log any session where the user claims a privileged identity

---

## 5. Layer 3 – Output Validation

**Goal:** Catch harmful content that the model generates before it reaches the user.

### 5.1 Toxicity Scoring
Run every model output through a toxicity classifier before delivery:
- **Tools:** Perspective API (Google), OpenAI Moderation API, or custom classifier
- **Threshold:** Block output scoring > 0.85 on any harmful category
- **Action:** Return a safe fallback response and log the incident

### 5.2 PII Detection & Redaction
- Scan outputs for personally identifiable information patterns (names + addresses, credit cards, etc.)
- Automatically redact or block any output containing PII not present in the original user input

### 5.3 Hallucination Guard (for RAG applications)
- For factual or document-based responses, validate that key claims are present in the retrieved source chunks
- Flag responses where the model generates specific facts not grounded in the provided context
- For legal / medical / financial applications: add disclaimer that all AI responses should be verified by a qualified professional

### 5.4 Demographic Bias Monitoring (Image Generation)
- Run a demographic classifier on batches of generated images periodically
- Alert if representation of any demographic group falls below 15% or exceeds 80% for neutral prompts
- Log prompt-to-demographic mappings for quarterly bias audits

---

## 6. Layer 4 – Human Oversight & Monitoring

**Goal:** Ensure humans remain in the loop and can catch systemic failures.

### 6.1 Audit Logging
Log the following for every interaction:
- Timestamp, session ID, user ID (hashed)
- Input prompt (after PII redaction)
- Layer 1 classification result
- Model response (truncated if needed)
- Layer 3 toxicity score
- Any flags triggered

Retain logs for minimum 90 days. Use structured logging for easy querying.

### 6.2 Human Review Queue
- Automatically route flagged interactions to a human review queue
- Prioritize: borderline Layer 1 classifications, high toxicity scores, escalation pattern detections
- SLA: human reviewers should process queue within 48 hours

### 6.3 Escalation Paths
Define clear escalation paths for:
- **User reports of harmful output** → Immediate review + model response update
- **Pattern of novel jailbreak success** → Security patch within 72 hours
- **Regulatory inquiry** → Legal team notified, logs preserved

### 6.4 Red Team Cadence
- **Monthly:** Automated regression tests against known attack patterns
- **Quarterly:** Manual red teaming by a dedicated team
- **Annually:** Third-party AI safety audit

---

## 7. Implementation Roadmap

| Phase | Actions | Timeline |
|-------|---------|----------|
| Phase 1 | Deploy Layer 1 blocklist + OpenAI Moderation API for output | Week 1–2 |
| Phase 2 | Add session rate limiting + context sanitization | Week 3–4 |
| Phase 3 | Implement full audit logging infrastructure | Week 5–6 |
| Phase 4 | Establish human review queue + escalation paths | Week 7–8 |
| Phase 5 | Quarterly red team cadence + bias monitoring | Ongoing |

---

## 8. Responsible AI Principles

This framework is grounded in the following core principles:

1. **Safety over performance** — A model that refuses edge cases is better than one that complies with harmful requests.
2. **Transparency** — Users should know they are interacting with an AI and understand its limitations.
3. **Accountability** — Every AI decision should be traceable, auditable, and correctable.
4. **Fairness** — AI outputs should not systematically disadvantage any group based on race, gender, religion, or other protected characteristics.
5. **Human oversight** — AI systems should always have a human escalation path for high-stakes decisions.

---

## 9. Conclusion

No single guardrail is sufficient. Defense-in-depth — multiple overlapping layers of protection — is the only reliable approach to AI safety in production systems. The 4-Layer Safety Stack proposed here provides a practical, scalable architecture that can be implemented incrementally and adapted as the threat landscape evolves.

Security is not a feature to be shipped. It is an ongoing commitment.

---

*Framework prepared as part of DecodeLabs Generative AI Industrial Training | Task 5: AI Safety & Bias Audit*
