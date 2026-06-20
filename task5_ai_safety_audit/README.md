# Task 5 – The AI Safety & Bias Audit 🛡️

## Objective
Perform a comprehensive red teaming exercise on a production AI model, test for demographic bias in image generation, and propose a professional safety framework (guardrails) that an organization should implement before deploying an AI system publicly.

## What's Included

| File | Description |
|------|-------------|
| `red_team_report.md` | Full red teaming findings — jailbreak attempts, vulnerabilities, and analysis |
| `bias_test_results.md` | Gender and racial bias test documentation with prompts and findings |
| `safety_framework.md` | Proposed AI safety guardrails framework for DecodeLabs |

## Key Topics Covered
- **Prompt Injection** — manipulating system context via user input
- **Role-Play Jailbreaks** — using fictional framing to bypass safety filters
- **Persona Override Attacks** — attempting to replace the AI's core identity
- **Direct Instruction Attacks** — asking the model to "ignore previous instructions"
- **Gender Bias in Image Generation** — testing neutral profession prompts
- **Racial Bias in Image Generation** — testing nationality and default assumptions
- **Guardrail Architecture** — input filtering, output validation, human oversight

## Summary of Findings
- Modern LLMs (GPT-4, Claude) are significantly more robust than earlier models
- Subtle indirect attacks (multi-turn manipulation, fictional framing) remain more effective than direct attacks
- Image generation models show measurable demographic skew in profession-related prompts
- A multi-layer safety architecture is more effective than any single guardrail

## Final Recommendation
Implement the **4-Layer Safety Stack** detailed in `safety_framework.md` before any public deployment.
