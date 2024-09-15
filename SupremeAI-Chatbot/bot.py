from botbuilder.core import ActivityHandler, TurnContext
from botbuilder.schema import ChannelAccount

class LegalInsightBot(ActivityHandler):
    async def on_message_activity(self, turn_context: TurnContext):
        return await turn_context.send_activity(f"You said: {turn_context.activity.text}")

    async def on_members_added_activity(
        self, members_added: [ChannelAccount], turn_context: TurnContext
    ):
        for member in members_added:
            if member.id != turn_context.activity.recipient.id:
                await turn_context.send_activity("Welcome to Legal Insight Hub!")