from flask import Flask, render_template, request
from botbuilder.core import BotFrameworkAdapterSettings, ConversationState, MemoryStorage
from botbuilder.schema import Activity
from botbuilder.core.integration import aiohttp_channel_service_routes, BotFrameworkHttpAdapter

from bot import LegalInsightBot

app = Flask(__name__)

# Bot Setup
SETTINGS = BotFrameworkAdapterSettings("", "")
ADAPTER = BotFrameworkHttpAdapter(SETTINGS)
CONVERSATION_STATE = ConversationState(MemoryStorage())
BOT = LegalInsightBot()

# Existing routes
@app.route('/')
def index():
    return render_template('index.html')

# ... other routes ...

# Bot endpoint
@app.route("/api/messages", methods=["POST"])
def messages():
    if "application/json" in request.headers["Content-Type"]:
        body = request.json
    else:
        return Response(status=415)

    activity = Activity().deserialize(body)
    auth_header = request.headers["Authorization"] if "Authorization" in request.headers else ""

    response = await ADAPTER.process_activity(activity, auth_header, BOT.on_turn)
    if response:
        return jsonify(response.body)
    return Response(status=201)

if __name__ == '__main__':
    app.run(debug=True)