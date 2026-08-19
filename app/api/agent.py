from fastapi import APIRouter, Depends
from schema.agent import AgentChatRequest, AgentChatResponse
from agents.engine import create_expense_agent
from core.dependency import get_current_user
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from core.exceptions import ExpenseException
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/agent", tags=["Agent"])

# Create the agent once at module load (it's stateless)
_agent = create_expense_agent()


@router.post("/chat", response_model=AgentChatResponse)
async def chat_with_agent(
    body: AgentChatRequest,
    current_user=Depends(get_current_user),
):
    """
    Chat with the Financial Copilot agent.
    The agent can add expenses, list expenses, and provide summaries.
    Categories are enforced to: Food, Transportation, Housing, Utilities,
    Entertainment, Health, Shopping, Others.
    """
    try:
        # Inject user_id into the message so tools can use it without
        # asking the LLM to guess it
        augmented_message = (
            f"[user_id={current_user.id}] {body.message}"
        )

        result = await _agent.ainvoke(
            {"messages": [HumanMessage(content=augmented_message)]}
        )

        messages = result.get("messages", [])

        # Extract the final AI text reply
        reply = ""
        for msg in reversed(messages):
            if isinstance(msg, AIMessage) and msg.content:
                reply = msg.content
                break

        # Collect names of tools that were invoked in this run
        tool_calls_made = []
        for msg in messages:
            if isinstance(msg, AIMessage) and msg.tool_calls:
                for tc in msg.tool_calls:
                    tool_calls_made.append(tc["name"])

        return AgentChatResponse(reply=reply, tool_calls_made=tool_calls_made)

    except ExpenseException as e:
        raise e
    except Exception as e:
        logger.error(f"Agent error: {e}", exc_info=True)
        raise ExpenseException(str(e))
