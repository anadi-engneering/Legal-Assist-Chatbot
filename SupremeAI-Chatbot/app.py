from flask import Flask, render_template, request, jsonify
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.cosmos import CosmosClient
from azure.ai.language.conversations import ConversationAnalysisClient
import os

app = Flask(__name__)

# Azure AI Search setup
search_endpoint = os.environ["AZURE_SEARCH_SERVICE_ENDPOINT"]
search_key = os.environ["AZURE_SEARCH_API_KEY"]
search_index_name = os.environ["AZURE_SEARCH_INDEX_NAME"]
search_credential = AzureKeyCredential(search_key)
search_client = SearchClient(search_endpoint, search_index_name, search_credential)

# Azure Cosmos DB setup
cosmos_endpoint = os.environ["COSMOS_ENDPOINT"]
cosmos_key = os.environ["COSMOS_KEY"]
cosmos_client = CosmosClient(cosmos_endpoint, cosmos_key)
database = cosmos_client.get_database_client("LegalAssistDB")
container = database.get_container_client("Conversations")

# Azure AI Language setup
ai_endpoint = os.environ["AZURE_AI_ENDPOINT"]
ai_key = os.environ["AZURE_AI_KEY"]
ai_client = ConversationAnalysisClient(ai_endpoint, AzureKeyCredential(ai_key))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_query = request.json['query']
    language = request.json['language']

    # Perform search using Azure AI Search
    search_results = search_client.search(user_query, top=3)
    context = " ".join([result['content'] for result in search_results])

    # Use Azure AI Language for response generation
    result = ai_client.analyze_conversation(
        task={
            "kind": "Conversation",
            "analysisInput": {
                "conversationItem": {
                    "text": user_query,
                    "id": "1",
                    "participantId": "user1"
                },
                "isLoggingEnabled": False
            },
            "parameters": {
                "projectName": "LegalAssistProject",
                "deploymentName": "production",
                "verbose": True
            }
        }
    )

    # Store conversation in Cosmos DB
    container.create_item({
        "id": str(result.conversation_id),
        "query": user_query,
        "response": result.prediction.top_intent,
        "language": language
    })

    return jsonify({
        "response": result.prediction.top_intent,
        "context": context
    })

if __name__ == '__main__':
    app.run(debug=True)