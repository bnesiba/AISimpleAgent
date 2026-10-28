# AISimpleAgent — Codebase Reader

An experimental coding agent built on [AISimpleAgent](https://github.com/bnesiba/AISimpleAgent), exploring codebase understanding, automated code modification, and agents that can extend their own tooling.

This project grew out of an earlier developer-productivity hackathon experiment focused on helping developers understand unfamiliar codebases. The new implementation expanded that concept beyond codebase exploration and documentation into making and verifying code changes.

## Capabilities

The agent can:

- Explore and understand a codebase, using its own implementation by default
- Locate and explain existing functionality
- Read and modify source files
- Verify changes
- Modify its own agent harness to add new tools and capabilities

## Self-Modifying Agent Experiment

One of the goals of this experiment was to explore whether a coding agent could understand and extend the software that provides its own capabilities.

Rather than simply giving the agent a fixed collection of tools, the experiment allowed it to inspect the implementation of those tools and make changes to its own codebase.

### Demonstration

**[Watch the agent implement and use a new tool](https://github.com/user-attachments/assets/fce51d7d-f4e1-496a-bb0c-11175360799c)**

In the recorded demonstration, the agent:

1. Examines and explains how its existing tools are implemented.
2. Implements a new tool within its own agent harness.
3. Uses the newly implemented tool.

The demonstration uses `llmagent-ui` for the interface.

## Implementation

Built in Python using LangGraph and the reusable agent infrastructure from AISimpleAgent.

The coding-agent implementation extends the base agent with tools for navigating, inspecting, modifying, and verifying source code. Because the agent can operate on its own repository, these capabilities can also be used to modify its underlying implementation.

For the reusable agent foundation and additional examples, see the [main AISimpleAgent repository](https://github.com/bnesiba/AISimpleAgent).

## Project Status

Experimental prototype developed in 2025, preserved as an example of my work exploring coding agents, extensible tooling, and agent architecture.

Not intended as a production-ready coding assistant.
