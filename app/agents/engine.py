from langgraph.prebuilt import create_react_agent
from core.llm import llm
from agents.tools import ExpenseToolkit
from agents.prompts import EXPENSE_AGENT_SYSTEM_PROMPT


def create_expense_agent():
    tools = [
        ExpenseToolkit.get_expenses,
        ExpenseToolkit.add_expense,
        ExpenseToolkit.get_expense_summary,
    ]

    agent_executor = create_react_agent(
        model=llm,
        tools=tools,
        prompt=EXPENSE_AGENT_SYSTEM_PROMPT,
    )

    return agent_executor