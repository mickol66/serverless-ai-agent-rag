import aws_cdk as core
import aws_cdk.assertions as assertions

from serverless_ai_agent_rag.serverless_ai_agent_rag_stack import ServerlessAiAgentRagStack

# example tests. To run these tests, uncomment this file along with the example
# resource in serverless_ai_agent_rag/serverless_ai_agent_rag_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = ServerlessAiAgentRagStack(app, "serverless-ai-agent-rag")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
