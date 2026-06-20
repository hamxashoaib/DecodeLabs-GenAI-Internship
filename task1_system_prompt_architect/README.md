# Task 1 – The System Prompt Architect 🧠

## Objective
Design a complex System Prompt that creates a strict AI persona for a high-end luxury travel agency. The AI must maintain a professional tone, know when to offer discounts, and never mention competitors.

## What's Included

| File | Description |
|------|-------------|
| `system_prompt.md` | Full system prompt with persona, constraints, and knowledge boundaries |
| `few_shot_examples.md` | Few-shot prompting examples demonstrating perfect AI responses |

## Key Techniques Used
- **Persona Engineering** – defined name, tone, role, and backstory
- **Hard Constraints** – competitor blacklist, discount logic, escalation rules
- **Few-Shot Prompting** – 4 example Q&A pairs training the model on ideal behavior
- **Knowledge Boundary Setting** – the AI knows what it can and cannot answer

## How to Test
Paste the contents of `system_prompt.md` as the system prompt in ChatGPT, Claude, or Gemini, then try the sample interactions from `few_shot_examples.md`.
