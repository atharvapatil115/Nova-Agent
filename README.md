# Nova

**Nova is a personal AI agent I'm building to interact with my email, voice, GitHub, and eventually my local system.**

The idea is simple: instead of building another chatbot, I want Nova to actually **do things** through tools.

The project is being built step-by-step, with security becoming more important as Nova gets access to more systems.

---

## Current Status

Nova currently has:

- LLM-based agent loop
- Multiple LLM providers with fallback routing
- Tool registry
- Gmail integration
- Read emails
- Read individual email threads/messages
- Create Gmail drafts
- Speech-to-text
- Text-to-speech
- Wake-word detection


## Complete System Architecture

```text
HOST MACHINE
     │
     │  Microphone / Speaker
     ▼
┌─────────────────────────────────────────────────────────────┐
│                    UBUNTU VM / SANDBOX                    │
│                                                             │
│   ┌───────────────┐                                         │
│   │  Voice Input  │                                         │
│   │  Wake Word    │                                         │
│   │  STT / Whisper│                                         │
│   └───────┬───────┘                                         │
│           │                                                 │
│           ▼                                                 │
│   ┌────────────────┐                                        │
│   │   NOVA AGENT   │                                        │
│   │                │                                        │
│   │ Understand     │                                        │
│   │ Plan           │                                        │
│   │ Maintain State │                                        │
│   └───────┬────────┘                                        │
│           │                                                 │
│           ▼                                                 │
│   ┌────────────────┐                                        │
│   │   LLM ROUTER   │                                        │
│   │                │                                        │
│   │ Provider A     │                                        │
│   │ Provider B     │                                        │
│   │ Provider C     │                                        │
│   └───────┬────────┘                                        │
│           │                                                 │
│           ▼                                                 │
│   ┌──────────────────────┐                                  │
│   │   PERMISSION LAYER   │                                  │
│   │                      │                                  │
│   │ Risk Check           │                                  │
│   │ Authorization        │                                  │
│   └──────────┬───────────┘                                  │
│              │                                              │
│        ┌─────┴─────┐                                        │
│        │           │                                        │
│      SAFE        RISKY                                      │
│        │           │                                        │
│        │           ▼                                        │
│        │    ┌────────────────┐                              │
│        │    │ USER CONFIRM   │                              │
│        │    └───────┬────────┘                              │
│        │            │                                       │
│        └─────┬──────┘                                       │
│              ▼                                              │
│   ┌──────────────────────┐                                  │
│   │    TOOL REGISTRY     │                                  │
│   └──────────┬───────────┘                                  │
│              │                                              │
│       ┌──────┼───────────┬─────────────┐                    │
│       ▼      ▼           ▼             ▼                    │
│    Gmail   GitHub    File System    Terminal               │
│       │      │           │             │                    │
│       └──────┴───────────┴─────────────┘                    │
│                       │                                     │
│                       ▼                                     │
│              ┌─────────────────┐                            │
│              │   TOOL RESULT   │                            │
│              └────────┬────────┘                            │
│                       │                                     │
│                       ▼                                     │
│              ┌─────────────────┐                            │
│              │   NOVA AGENT    │                            │
│              │ Interpret result│                            │
│              │ Continue / Done │                            │
│              └────────┬────────┘                            │
│                       │                                     │
│                       ▼                                     │
│              ┌─────────────────┐                            │
│              │  TTS / RESPONSE │                            │
│              └────────┬────────┘                            │
│                       │                                     │
└───────────────────────┼─────────────────────────────────────┘
                        │
                        ▼
                 HOST SPEAKER
```

The basic loop is:

```text
User
 ↓
Nova
 ↓
LLM
 ↓
Tool
 ↓
Tool Result
 ↓
Nova
 ↓
Response
```

---

# Gmail

Gmail is the first external service Nova is connected to.

Currently Nova can:

- Read recent/unread emails
- Read individual emails
- Create Gmail drafts

Sending emails is intentionally not enabled yet.

The plan is to add sending later with an explicit confirmation step.

---

# Voice

Nova is designed to be voice-first.

```text
Microphone
    ↓
Wake Word
    ↓
Speech-to-Text
    ↓
Nova
    ↓
Text-to-Speech
    ↓
Speaker
```

Current voice stack:

- Whisper for speech recognition
- ElevenLabs for voice output
- OpenWakeWord for wake-word detection

---

# LLM Routing

Nova doesn't depend on a single LLM provider.

The agent talks to an internal LLM router:

```text
              Nova
                │
                ▼
           LLM Router
          /     |     \
         ▼      ▼      ▼
      Model A Model B Model C
```

If one provider isn't available, another provider can be used.

This also keeps the agent code independent from a specific LLM provider.

---

# Project Structure

```text
Nova-Agent/
│
├── app/
│   ├── agent/
│   ├── ai/
│   ├── llm/
│   ├── gmail/
│   └── voice/
│
├── audio/
├── credentials/
├── .env
├── .gitignore
└── README.md
```

The project is intentionally split into separate modules so new tools can be added without turning the agent into one large file.

---

# What's Next?

The next major step isn't another feature.

It's **sandboxing Nova**.

Nova will eventually have access to things like:

```text
Gmail
GitHub
Files
Terminal
Local system
```

Giving an LLM unrestricted access to those things isn't something I want to do directly on my main Windows system.

So the next stage is:

```text
Windows Host
     │
     ▼
 Ubuntu VM
     │
     ▼
   Nova
     │
 ┌───┼────┬──────┐
 ▼   ▼    ▼      ▼
Gmail GitHub Files System
```

The VM will become Nova's controlled environment.

---

# Planned Features

### Agent

- Persistent conversation state
- Long-term memory
- Better task planning
- Multi-step tool execution
- Background tasks

### Gmail

- Email summaries
- Search
- Thread handling
- Draft editing
- Send with confirmation
- New-email notifications

### GitHub

- Read repositories
- Inspect files
- Read issues
- Create/edit files
- Controlled commits and pushes

### System

- Controlled filesystem access
- Terminal commands
- Application launching
- Automation

### Voice

- Custom `Nova` wake word
- Better interruption handling
- More natural conversations

### Security

- Ubuntu sandbox
- Permission system
- Risk-based tool approval
- Tool-level restrictions
- Separate test accounts

---

# Security

Nova is still experimental.

For now, it should **not** have unrestricted access to personal accounts, sensitive files, or the host operating system.

As the project grows, tools will go through a permission layer before they are allowed to perform sensitive actions.

The goal is to make Nova more capable **without giving the LLM unrestricted control over everything around it.**

---

# Tech Stack

- Python
- Pydantic
- Gmail API
- Whisper
- ElevenLabs
- OpenWakeWord
- Multiple LLM providers
- Git / GitHub

---

# Roadmap

```text
[✓] Agent foundation
[✓] LLM routing
[✓] Tool registry
[✓] Gmail integration
[✓] Voice pipeline

[ ] Ubuntu sandbox
[ ] Permission system
[ ] Dedicated test accounts
[ ] GitHub tools
[ ] System tools
[ ] Memory
[ ] Event-driven agent
[ ] More autonomous workflows
```

