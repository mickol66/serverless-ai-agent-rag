import json
import boto3
import os

# Initiera Bedrock-klienten utanför handlern så den återanvänds mellan anrop (sparar tid!)
bedrock_client = boto3.client(service_name="bedrock-runtime", region_name="eu-north-1")

def handler(event, context):
    try:
        # 1. Hämta frågan från API Gateway-anropets body
        body = json.loads(event.get("body", "{}"))
        user_question = body.get("question", "Hello! Who are you?")

        # 2. Ange vilken modell vi vill prata med (Claude 3 Haiku)
        #model_id = "anthropic.claude-3-haiku-20240307-v1:0"
        model_id = "eu.anthropic.claude-4-5-haiku-20260210-v1:0"
        # 3. Strukturera anropet enligt Anthropics gällande format
        native_request = {
            "anthropic_version": "bedrock-2023-05-31",
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

        # Convert payload to JSON string
        request_body = json.dumps(native_request)

        # 4. Anropa Amazon Bedrock via Boto3 [5.1]
        response = bedrock_client.invoke_model(
            modelId=model_id,
            body=request_body
        )

        # 5. Läs av och avkoda svaret från modellen
        response_body = json.loads(response.get("body").read())
        ai_response_text = response_body["content"]["text"]

        # 6. Returnera ett korrekt strukturerat svar med CORS-headers aktiverade
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*" # Tillåter anrop från din portfoliowebbplats
            },
            "body": json.dumps({
                "question": user_question,
                "answer": ai_response_text,
                "model_used": "Anthropic Claude 3 Haiku"
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
