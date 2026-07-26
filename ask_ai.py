import requests
import json

# 1. Klistra in din URL från CloudFormation här (och lägg till 'ask' på slutet så den slutar på /prod/ask)
API_URL = "https://gcw6hn3oyk.execute-api.eu-north-1.amazonaws.com/prod/ask"

# 2. Skriv den fråga du vill ställa till din AI-agent!
payload = {
    "question": "Hello Claude! Can you explain what AWS services were used to build you, and why this architecture is highly secure?"
}

print(f"🧠 Sending question to your Serverless AI Agent...")

try:
    response = requests.post(
        API_URL,
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    
    if response.status_code == 200:
        result = response.json()
        print("\n🤖 AI Response:")
        print("-" * 50)
        print(result["answer"])
        print("-" * 50)
        print(f"Model used: {result['model_used']}")
    else:
        print(f"\n❌ Error: Received status code {response.status_code}")
        print(response.text)

except Exception as e:
    print(f"\n❌ Failed to connect to API: {str(e)}")
