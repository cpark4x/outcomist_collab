"""Claude AI agent integration."""

from anthropic import Anthropic

from ..config import settings
from ..database.models import Message
from ..database.models import MessageRole
from ..database.models import Project


class ClaudeAgent:
    """Claude AI agent for conversations."""

    def __init__(self):
        """Initialize Claude agent."""
        self.client = Anthropic(api_key=settings.anthropic_api_key)

    def send_message(
        self,
        project: Project,
        conversation_history: list[Message],
        user_message: str,
    ) -> str:
        """Send message to Claude and get response.

        Args:
            project: The project context
            conversation_history: Previous messages in the session
            user_message: The user's message

        Returns:
            Claude's response text
        """
        from .prompts import get_system_prompt

        # Build messages array for Claude API
        messages = []

        # Add conversation history (exclude system messages)
        for msg in conversation_history:
            if msg.role != MessageRole.SYSTEM:
                messages.append({"role": msg.role.value, "content": msg.content})

        # Add current user message
        messages.append({"role": "user", "content": user_message})

        # Get system prompt for project type
        system_prompt = get_system_prompt(project.type)

        # Call Claude API
        response = self.client.messages.create(
            model=settings.claude_model,
            max_tokens=settings.claude_max_tokens,
            temperature=settings.claude_temperature,
            system=system_prompt,
            messages=messages,
        )

        # Extract text from response
        return response.content[0].text


# Global agent instance
agent = ClaudeAgent()
