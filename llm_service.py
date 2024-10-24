"""
Defines the LLMService class for executing commands using a language model.

Classes:
    - LLMService: A service for executing commands using a language model.
"""

import uuid
from langchain_community.tools.shell import ShellTool
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableConfig
from langgraph.graph.graph import CompiledGraph
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from config import get_steps_file, get_llm_key
from models.models import LLMResponse


class LLMService:
    """
    Acts as an interface to the Large Language Model.
    """

    def __init__(self):
        llm = ChatOpenAI(
            model="gpt-4o",
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2,
            api_key=get_llm_key(),
        )
        shell_tool = ShellTool()
        tools = [shell_tool]
        memory = MemorySaver()
        self.agent_executor: CompiledGraph = create_react_agent(
            llm, tools, checkpointer=memory
        )

    @staticmethod
    def _get_human_readable_agent_response(agent_response: dict) -> str:
        """
        Extracts the human-readable summary from the agent response.
        :param agent_response:
        :return: str: A short summary of the agent response.
        """
        summary: str = ""

        if "agent" in agent_response:
            messages = agent_response["agent"]["messages"]
            for message in messages:
                tool_calls = message.additional_kwargs.get("tool_calls", [])
                if tool_calls:
                    for tool_call in tool_calls:
                        command = tool_call.get("function", {}).get("arguments", "")
                        # Extract and format the command
                        summary = (
                            f"Executing command:\n{command.split(':')[1].strip(' }')}"
                        )

                else:
                    content = message.content
                    if content:
                        # If content exists, simply append it without prefix
                        summary = content.strip()

        elif "tools" in agent_response:
            messages = agent_response["tools"]["messages"]
            for message in messages:
                content = message.content
                # Format tool output
                summary = f"Command output:\n{content.strip() if content else ''}"

        return summary

    async def execute(self, user_input: str) -> LLMResponse:
        """
        Executes a user command using the language model.
        :param user_input:
        :return: dict: final message after processing the user command.
        """
        session_id: str = str(uuid.uuid4())
        steps_file = get_steps_file(session_id)
        try:
            with open(steps_file, "a", encoding="utf-8") as f:
                f.write("User input:\n" + user_input + "\n")

                config: RunnableConfig = {"configurable": {"thread_id": session_id}}
                final_message = "User command processed."
                for chunk in self.agent_executor.stream(
                    input={"messages": [HumanMessage(content=user_input)]},
                    config=config,
                ):
                    f.write(
                        "----------------------\n"
                        + self._get_human_readable_agent_response(chunk)
                        + "\n"
                    )
                    final_message = self._get_human_readable_agent_response(chunk)
            return LLMResponse(msg=final_message, session_id=session_id)
        except Exception as e:
            raise RuntimeError(f"Failed to execute user command: {str(e)}") from e
