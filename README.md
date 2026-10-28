# AISimpleAgent

A simple, extensible, ready-to-use AI agent built with Python and LangGraph.

Designed as a reusable starting point for experimenting with tool-using agents without having to rebuild the basic agent infrastructure each time. Includes examples demonstrating custom tools, metadata, streaming, and other agent capabilities.

## Codebase Reader / Self-Modifying Agent

The [codebase-reader branch](https://github.com/bnesiba/AISimpleAgent/tree/codebase-reader) contains an experimental coding agent built on AISimpleAgent.

The agent can navigate a codebase (its own by default), inspect and modify files, and verify changes.

Experimentally the agent was able to extend its own capabilities by modifying the harness it was running on. In the demonstration, the agent explains the functionality it needs, implements a new tool in its own codebase, and then successfully uses that tool.

[[Watch the demonstration]](https://github.com/user-attachments/assets/fce51d7d-f4e1-496a-bb0c-11175360799c) — Agent implementing and using a new tool for itself.

The demonstration uses llmagent-ui for the interface.

## Project Status

Originally developed in 2025 as an experimental agent foundation and a way to explore tool-using and self-modifying coding agents. This repository is preserved as an example of those experiments rather than as a production-ready coding assistant.
