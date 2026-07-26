import json
import boto3

# Initiera Bedrock-klienterna i Stockholm
bedrock_client = boto3.client(service_name="bedrock", region_name="eu-north-1")
bedrock_runtime = boto3.client(service_name="bedrock-runtime", region_name="eu-north-1")

def handler(event, context):
    try:
        # LOGGNING FÖR ATT HITTA RÄTT ID:
        # Vi listar alla tillgängliga modeller i ditt konto och skriver ut i CloudWatch
        print("🔍 Listing all available foundation models in eu-north-1:")
        models = bedrock_client.list_foundation_models()
        for model in models.get('modelSummaries', []):
            if 'anthropic' in model.get('modelId', ''):
                print(f"-> Giltigt ID: {model.get('modelId')} (Status: {model.get('modelLifecycle', {}).get('status')})")

        # Hämta frågan från API Gateway
        body = json.loads(event.get("body", "{}"))
        user_question = body.get("question", "Hello! Who are you?")

        # Vi testar det universella och mest stabila bas-ID:t för Claude 3 Haiku
        # model_id = "anthropic.claude-3-haiku-20240307-v1:0"
        model_id = "anthropic.claude-haiku-4-5-20251001-v1:0"

        # NYA CONVERSE API: Det moderna sättet att prata med Bedrock (ersätter invoke_model)
        # Det hanterar payloads mycket säkrare och minskar risken för ValidationException
        response = bedrock_runtime.converse(
            modelId=model_id,
            messages=[
                {
                    "role": "user",
                    "content": [{"text": user_question}]
                }
            ],
            inferenceConfig={
                "maxTokens": 512,
                "temperature": 0.5
            }
        )

        # Hämta ut textsvaret från det nya formatet
        ai_response_text = response["output"]["message"]["content"][0]["text"]

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({
                "question": user_question,
                "answer": ai_response_text,
                "model_used": model_id
            })
        }

    except Exception as e:
        print(f"❌ Detailed Error: {str(e)}")
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({"error": "Failed to generate AI response", "details": str(e)})
        }
