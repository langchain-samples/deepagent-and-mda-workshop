from langchain.agents.middleware import TodoListMiddleware
from managed_deepagents import define_deep_agent

from middleware.audit import log_tool_calls
from tools.search import tavily_search

# Sync subagent: the agent calls it with `task` and waits for the answer.
fact_checker = {
    "name": "fact-checker",
    "description": "Checks a draft report's claims against the web before it is finalized.",
    "system_prompt": (
        "You are a meticulous fact-checker. Verify each factual claim in the draft with "
        "tavily_search. Reply with a short list of claims that are unsupported or wrong, "
        "with the correction and a source URL. If every claim checks out, say so."
    ),
    "tools": [tavily_search],
}

# Async subagent: the agent starts it with `start_async_task` and keeps talking to the
# user. It runs as its own graph (research-agent--deep-researcher) and reports back when
# it finishes. Keep `name` and `async` literal: MDA reads them from this file at build time.
deep_researcher = {
    "name": "deep-researcher",
    "description": (
        "Runs a long, in-depth research job in the background (many searches, following "
        "links in the browser). Use for broad or multi-part topics so you can keep "
        "chatting with the user while it works."
    ),
    "system_prompt": (
        "You are a thorough background researcher. Use tavily_search to find sources, then "
        "open the most promising pages with the browser tools (browser_run to navigate, "
        "browser_snapshot to read) to pull details that search snippets miss. Write your "
        "findings to /workspace/research/<topic-slug>.md with numbered citations, and reply "
        "with a concise summary plus the file path."
    ),
    "tools": [tavily_search],
    "async": True,
}

agent = define_deep_agent(
    name="research-agent",
    model="openai:gpt-6.1-sol",
    tools=[tavily_search],
    middleware=[log_tool_calls, TodoListMiddleware()],  # TodoListMiddleware adds write_todos
    subagents=[fact_checker, deep_researcher],
)
