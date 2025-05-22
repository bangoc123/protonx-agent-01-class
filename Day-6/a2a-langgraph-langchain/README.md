### A2A Protocol + LangGraph

![](https://storage.googleapis.com/mle-courses-prod/users/61b6fa1ba83a7e37c8309756/private-files/00f44750-36cd-11f0-a0e3-6fefe2bf1875-Screenshot_2025_05_22_122401.png)

## 🚀 Getting Started

This guide will walk you through installing the necessary tools, running the server, and testing the agent.

-----

### 1\. Installation 🛠️

First, you'll need to install `uv`, a fast Python package installer and resolver.

```bash
pip install uv
```

Next, install the required libraries specified in your `pyproject.toml` file using `uv`.

```bash
uv pip sync pyproject.toml
```

-----

### 2\. Running the Server 🖥️

To start the main server, run the following command:

```bash
uv run .
```

The server will be accessible at `http://localhost:10000`.

You can check the agent's status by navigating to:
`http://localhost:10000/.well-known/agent.json`

![](https://storage.googleapis.com/mle-courses-prod/users/61b6fa1ba83a7e37c8309756/private-files/bf4ae860-36c5-11f0-942a-a32fda0d8c1e-Screenshot_2025_05_22_113210.png)

-----

### 3\. Testing the Agent 🧪

To test your agent, execute the following script:

```bash
python test_agent.py
```

-----

### 4\. Running A2A (Agent-to-Agent) Components 🤝

#### A2A Server

To run the A2A server component, use the same command as the main server:

```bash
uv run .
```

#### A2A Client

```bash
uv run a2a_client.py
```

![](https://storage.googleapis.com/mle-courses-prod/users/61b6fa1ba83a7e37c8309756/private-files/e569d1a0-36c5-11f0-a0e3-6fefe2bf1875-Screenshot_2025_05_22_113313.png)

*(Instructions for running the A2A client seem to be missing from the original text, other than the image. You might want to add the specific command here if available.)*