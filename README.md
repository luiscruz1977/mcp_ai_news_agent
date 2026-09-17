# AI News Agent

A small, practical project built to explore two concepts that are
becoming increasingly important in modern AI applications: **Agentic
AI** and the **Model Context Protocol (MCP)**.

The application uses Gemini as the reasoning model and an MCP Fetch
Server as the agent's external web access capability. A lightweight
Streamlit interface provides a simple way for a user to interact with
the agent.

The project deliberately keeps the architecture small. The goal is not
to build a production news platform, but to understand how an AI agent
can decide when it needs an external tool, invoke that tool through MCP, use the retrieved information, and produce a final answer.

------------------------------------------------------------------------

## Project Goals

The main goal of this project is learning by building.

The project focuses on:

-   Understanding the basic architecture of an AI agent
-   Understanding tool calling with an LLM
-   Understanding the role of MCP
-   Implementing an MCP client in Python
-   Using an MCP server to access external information
-   Observing the agent's decision and tool usage
-   Building a simple user interface with Streamlit
-   Keeping the architecture understandable and easy to extend

The project intentionally avoids frameworks and infrastructure that are
not necessary for this learning objective.

------------------------------------------------------------------------

## What the Application Does

The application acts as a small AI news and research assistant.

A user can ask a question such as:

> What are the latest AI developments from OpenAI, Anthropic and Google?

The Gemini model receives the question and has access to a `fetch` tool.

When external information is needed, the agent can request the tool. The MCP client sends that request to the Fetch MCP Server, which retrieves the requested web page.

The retrieved content is then provided to Gemini, which analyses the
information and generates the final response.

The Streamlit interface also displays the agent activity, making the
process visible to the user.

------------------------------------------------------------------------

## Architecture

The current architecture is intentionally simple:

``` text
┌──────────────────────────┐
│        User              │
│                          │
│   Streamlit Interface    │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│       Gemini Agent       │
│                          │
│  Reasoning + Tool Call   │
└────────────┬─────────────┘
             │
             │ MCP
             ▼
┌──────────────────────────┐
│       MCP Client         │
│                          │
│     mcp_client.py        │
└────────────┬─────────────┘
             │
             │ stdio
             ▼
┌──────────────────────────┐
│    Fetch MCP Server      │
│                          │
│       fetch(url)         │
└────────────┬─────────────┘
             │
             │ HTTP
             ▼
┌──────────────────────────┐
│       Web Sources        │
│                          │
│ OpenAI / Anthropic /     │
│ Google AI                │
└──────────────────────────┘
```

### Component responsibilities

#### Streamlit

`app.py` provides the graphical interface.

It is responsible for:

-   Receiving the user's question
-   Starting the agent
-   Displaying the agent activity
-   Displaying the final answer

Streamlit was chosen because it provides a simple UI without requiring a
separate frontend application.

#### Gemini

Gemini is the reasoning model used by the application.

The model receives the user's question and has access to a declared
`fetch` tool.

The important point is that the application does not automatically fetch
a web page for every question. Gemini can decide whether external
information is required.

This gives the application a basic agentic behaviour.

#### MCP Client

`mcp_client.py` contains the code responsible for communicating with the
MCP server.

The client:

1.  Starts the Fetch MCP Server
2.  Establishes an MCP session
3.  Initializes the session
4.  Calls the `fetch` tool
5.  Receives the result
6.  Returns the retrieved content to the agent

The client does not implement web scraping itself. It delegates that
capability to the MCP server.

#### Fetch MCP Server

The Fetch MCP Server provides the external capability used by the agent.

Its main operation is:

``` text
fetch(url)
```

The server retrieves the content of a web page and returns it to the MCP client.

This is the part of the architecture that demonstrates the value of MCP: the agent can use an external capability through a standard protocol without having to implement that capability itself.

#### Web Sources

The initial project uses three AI related sources:

``` text
OpenAI
https://openai.com/news/

Anthropic
https://www.anthropic.com/news

Google AI
https://blog.google/technology/ai/
```

These sources provide the content that the agent can retrieve and
analyse.

------------------------------------------------------------------------

## How the Agent Works

The basic execution flow is:

``` text
1. User asks a question
              │
              ▼
2. Gemini receives the question
              │
              ▼
3. Gemini decides whether external information is required
              │
        ┌─────┴─────┐
        │           │
       No          Yes
        │           │
        ▼           ▼
   Answer      Request fetch tool
                    │
                    ▼
              MCP Client
                    │
                    ▼
             Fetch MCP Server
                    │
                    ▼
                  Web
                    │
                    ▼
             Retrieved content
                    │
                    ▼
              Gemini analyses
                    │
                    ▼
               Final answer
```

This distinction is important.

A traditional application might simply execute:

``` text
question → HTTP request → result
```

In this project, the model participates in deciding whether a tool is
needed:

``` text
question → agent reasoning → tool decision → MCP tool → result → reasoning → answer
```

That is the main agentic concept demonstrated by the project.

------------------------------------------------------------------------

## Understanding MCP in This Project

MCP stands for **Model Context Protocol**.

In this project, MCP provides a standard way for the AI application to
communicate with an external capability.

The important separation is:

``` text
Gemini
  │
  │ decides what it needs
  ▼
MCP Client
  │
  │ communicates using MCP
  ▼
MCP Server
  │
  │ provides the capability
  ▼
Fetch
```

The Gemini model does not directly contain the implementation of the
Fetch capability.

The MCP server provides that capability independently.

This separation makes it easier to understand how tools can be exposed
to AI agents through a common protocol.

------------------------------------------------------------------------

## Agent Activity

The application exposes the agent's activity in the Streamlit interface.

For example:

``` text
🤖 Agent decided to use Fetch
🔧 Calling MCP Fetch Server
🌐 Fetching: https://...
✓ Content retrieved from MCP
📝 Agent generated final response
```

If external information is not required, the application can show:

``` text
🤖 Agent answered directly
✓ MCP was not required
```

This is intentionally simple, but it is useful for learning because it
makes the agent's behaviour visible rather than hiding everything behind
a final answer.

------------------------------------------------------------------------

## Project Structure

``` text
ai-news-agent/
│
├── .venv/
│
├── .env
├── .gitignore
├── requirements.txt
├── app.py
├── agent.py
├── mcp_client.py
├── README.md
│
├── agent_test.py
└── mcp_test.py
```

### Files

  File                 Purpose
  -------------------- -----------------------------------------------------
  `app.py`             Streamlit user interface
  `agent.py`           Gemini agent and tool calling logic
  `mcp_client.py`      MCP client and Fetch server communication
  `agent_test.py`      Basic agent testing
  `mcp_test.py`        Isolated MCP testing
  `.env`               Local Gemini API key
  `.gitignore`         Prevents sensitive/local files from being committed
  `requirements.txt`   Python dependencies
  `README.md`          Project documentation


------------------------------------------------------------------------

## Requirements

The project requires:

-   Python 3.10 or later
-   VS Code or another Python IDE
-   A Gemini API key
-   Internet access
-   `uv`, used to launch the Fetch MCP Server

The Python dependencies are defined in:

``` text
requirements.txt
```

Example:

``` text
google-genai
streamlit
python-dotenv
mcp>=1.29,<2
```

------------------------------------------------------------------------

## Configuration

Create a `.env` file in the project root:

``` env
GEMINI_API_KEY=your_gemini_api_key
```

The API key should never be committed to Git.

The `.gitignore` file should therefore include:

``` text
.env
.venv/
__pycache__/
```

------------------------------------------------------------------------

## Running the Application

Create and activate the virtual environment:

``` powershell
python -m venv .venv
```

Activate it on Windows:

``` powershell
.venv\Scripts\Activate.ps1
```

Install the dependencies:

``` powershell
pip install -r requirements.txt
```

Run the application:

``` powershell
streamlit run app.py
```

Streamlit will start the local web application and provide the address
to open in the browser.

------------------------------------------------------------------------

## Testing

The project contains two simple test scripts.

### Test the MCP connection

``` powershell
python mcp_test.py
```

This test bypasses Gemini and Streamlit and verifies the communication
between the Python MCP client and the Fetch MCP Server.

### Test the Agent

``` powershell
python agent_test.py
```

This verifies the Gemini agent and its interaction with the MCP Fetch
tool.

Keeping these tests separate is useful because it allows MCP and agent
problems to be isolated.

------------------------------------------------------------------------

## Example Questions

The application can be tested with questions such as:

``` text
What is Agentic AI?
```

The agent can answer directly without external information.

Another example:

``` text
What are the main concepts explained on
https://modelcontextprotocol.io/introduction?
```

In this case, the agent can use the Fetch tool to retrieve the page
before answering.

For the intended AI news use case:

``` text
What are the latest AI developments from OpenAI, Anthropic and Google?
```

The agent can use the configured AI sources and summarise the retrieved
information.

------------------------------------------------------------------------

## Why This Architecture?

The architecture was deliberately kept small.

There are many frameworks available for building agentic applications,
but introducing additional abstraction layers would make it harder to
understand what is actually happening.

This project therefore uses:

``` text
Python
+
Gemini
+
MCP
+
Fetch MCP Server
+
Streamlit
```

There is no LangChain, CrewAI, vector database, RAG pipeline, database
or cloud infrastructure in the initial version.

This keeps the learning path focused on the two concepts that matter
most for this project:

**Agentic AI and MCP.**

------------------------------------------------------------------------

## Key Learning Outcomes

After completing this project, the main concepts demonstrated are:

### 1. Tool Calling

The LLM can be given a description of an available tool and can request
that tool when appropriate.

### 2. Agentic Decision Making

The model is not limited to producing an immediate answer. It can decide
that additional information is required and request an external
capability.

### 3. MCP Client

The Python application acts as an MCP client and communicates with the
MCP server.

### 4. MCP Server

The Fetch server exposes an external capability through MCP.

### 5. Separation of Responsibilities

Each component has a clear responsibility:

``` text
Streamlit → user interaction

Gemini → reasoning

MCP Client → protocol communication

MCP Server → external capability

Web → external information
```

### 6. Observable Agent Behaviour

The interface exposes the agent's actions, making the tool calling
process easier to understand and demonstrate.

------------------------------------------------------------------------

## Design Philosophy

This project follows a simple principle:

> Build the smallest useful system that makes the concept visible.

The intention is not to maximise the number of technologies or features.

A small architecture is particularly valuable for learning because each
component can be understood individually and then connected to the next
one.

------------------------------------------------------------------------

## Possible Future Extensions

The current version is intentionally limited.

If the project is extended later, possible directions include:

-   Web search through another MCP server
-   Additional MCP tools
-   More structured news summaries
-   Source ranking or relevance filtering
-   Evaluation of agent responses
-   Scheduled news summaries
-   Persistent history
-   More sophisticated agent workflows

These are intentionally outside the scope of the initial implementation.

------------------------------------------------------------------------

## Conclusion

AI News Agent is a small hands-on demonstration of how an LLM based
agent can interact with the outside world through MCP.

The most important idea is not the news summarisation itself. It is the
architecture behind it:

``` text
User
 ↓
Agent
 ↓
Tool decision
 ↓
MCP Client
 ↓
MCP Server
 ↓
External capability
 ↓
Agent
 ↓
Final answer
```

By keeping the implementation deliberately simple, the project provides
a practical foundation for understanding how **Agentic AI and MCP fit
together** before moving on to more complex agent architectures.
