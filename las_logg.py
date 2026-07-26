import boto3

client = boto3.client('logs', region_name='eu-north-1')

try:
    response = client.get_log_events(
        logGroupName="/aws/lambda/ServerlessAiAgentStack-AiAgentBackendLambdaF277F7A-TGIBvBnDjUEb",
        logStreamName="2026/07/26/[$LATEST]b8ec8ea0fcab405ea686191b79ae677d",
        limit=50
    )
    
    print("\n--- INNEHÅLLET I DINA CLOUDWATCH-LOGGAR ---")
    for event in response.get('events', []):
        msg = event.get('message', '')
        # Vi rensar bort emojier manuellt så Windows inte kraschar vid utskrift!
        clean_msg = msg.encode('ascii', 'ignore').decode('ascii')
        if clean_msg.strip():
            print(clean_msg.strip())
            
except Exception as e:
    print(f"Fel vid hämtning: {str(e)}")
