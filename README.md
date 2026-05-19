# Message Cleaner Skill Experiment

This repository is a small prototype for experimenting with AI skill framework concepts before applying them to a larger project.

The goal is not to build a production-ready system yet. Instead, this repo uses a simple `message-cleaner` skill to explore how AI capabilities could be structured, versioned, adapted, and managed across different AI tools.

## Test Skill: Message Cleaner

The current test skill cleans and reformats rough Slack, Teams, or internal messages into clearer, more natural communication.

The skill is intentionally simple so the focus stays on testing the framework concepts around it.

### Example

Input:

```text
hey can u check the deploy thing idk if prod is broken but logs look weird maybe ask alex
```

Output:

```text
Hey Alex, could you take a quick look at the deployment? I noticed some unusual logs and want to confirm whether production is affected.
```
