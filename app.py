#!/usr/bin/env python3
import aws_cdk as cdk

# Importera din nyskapade AI-stack (dubbelkolla att namnet matchar din fil)
from serverless_ai_agent_rag.serverless_ai_agent_rag_stack import ServerlessAiAgentRagStack

app = cdk.App()

# Initiera din Serverlösa AI-Agent Stack
ServerlessAiAgentRagStack(
    app, "ServerlessAiAgentStack",
    # Vi låser regionen till Stockholm där Bedrock och Claude 3 finns redo
    env=cdk.Environment(region="eu-north-1")
)

app.synth()
