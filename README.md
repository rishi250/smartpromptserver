# SmartPromptServer

SmartPromptServer is a Python application that allows users to spin up a server to collect prompt responses from a chat-based application and store the history as context. This context can then be fetched to retrieve the most relevant context for further processing. Relevancy is determined by a Language Model (LLM), and the server is LLM-agnostic, meaning any model supported by the `litellm` package can be used.

## Features

- Spin up a server to collect prompt responses.
- Store prompt history as context.
- Fetch the most relevant context using an LLM.
- LLM-agnostic: Compatible with any model supported by `litellm` package.