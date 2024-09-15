import os

# Azure AI Search Configuration
AZURE_SEARCH_SERVICE_ENDPOINT = os.environ.get("AZURE_SEARCH_SERVICE_ENDPOINT")
AZURE_SEARCH_INDEX_NAME = os.environ.get("AZURE_SEARCH_INDEX_NAME")
AZURE_SEARCH_API_KEY = os.environ.get("AZURE_SEARCH_API_KEY")

# Azure Cosmos DB Configuration
COSMOS_ENDPOINT = os.environ.get("COSMOS_ENDPOINT")
COSMOS_KEY = os.environ.get("COSMOS_KEY")

# Azure AI Language Configuration
AZURE_AI_ENDPOINT = os.environ.get("AZURE_AI_ENDPOINT")
AZURE_AI_KEY = os.environ.get("AZURE_AI_KEY")

# Ensure all required environment variables are set
required_vars = [
    "AZURE_SEARCH_SERVICE_ENDPOINT",
    "AZURE_SEARCH_INDEX_NAME",
    "AZURE_SEARCH_API_KEY",
    "COSMOS_ENDPOINT",
    "COSMOS_KEY",
    "AZURE_AI_ENDPOINT",
    "AZURE_AI_KEY"
]

for var in required_vars:
    if not locals()[var]:
        raise EnvironmentError(f"Required environment variable {var} is not set")