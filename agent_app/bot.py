from botbuilder.core import ActivityHandler, TurnContext
from botbuilder.schema import ActivityTypes


class SimpleAgent(ActivityHandler):

    async def on_message_activity(self, turn_context: TurnContext):
        user_text = turn_context.activity.text

        reply = f"You said: {user_text}"
        await turn_context.send_activity(reply)

    async def on_members_added_activity(self, members_added, turn_context):
        for member in members_added:
            if member.id != turn_context.activity.recipient.id:
                await turn_context.send_activity("Hello! I am your Python Agent 🤖")
