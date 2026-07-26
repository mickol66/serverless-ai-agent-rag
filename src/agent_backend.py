import json
import boto3
import os

# Initiera Bedrock-klienten utanför handlern (eu-north-1)
bedrock_client = boto3.client(service_name="bedrock-runtime", region_name="eu-north-1")

def handler(event, context):
    try:
        body = json.loads(event.get("body", "{}"))
        user_question = body.get("question", "Hello! Who are you?")

        # 1. DET OFFICIELLA OCH SKOTTSÄKRA MODELL-ID:T FÖR CLAUDE 3.5 SONNET I EUROPA
        # Detta är den universella sträng som AWS STS och Bedrock garanterat känner igen i eu-north-1
        model_id = "anthropic.claude-3-5-sonnet-20240620-v1:0"
        
        # 2. Strukturera anropet enligt Anthropics stabila standardformat
        native_request = {
            "anthropic_version": "bedrock-2023-05-31", # Stabilt bas-datum för Claude 3/3.5
            "max_tokens": 512,
            "temperature": 0.5,
            "messages": [
                {
                    "role": "user",
                    "content": user_question
                }
            ],
            "system": "You are an advanced, helpful AI Portfolio Assistant. Answer clearly and professionally."
        }

        request_body = json.dumps(native_request)

        # 3. Anropa Amazon Bedrock [5.1]
        response = bedrock_client.invoke_model(
            modelId=model_id,
            body=request_body
        )

        response_body = json.loads(response.get("body").read())
        ai_response_text = response_body["content"]["text"]

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({
                "question": user_question,
                "answer": ai_response_text,
                "model_used": "Anthropic Claude 3.5 Sonnet"
            })
        }

    except Exception as e:
        print(f"❌ Error invoking Amazon Bedrock: {str(e)}")
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({"error": "Failed to generate AI response", "details": str(e)})
        }
