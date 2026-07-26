from aws_cdk import (
    Stack,
    RemovalPolicy,
    aws_s3 as s3,
    aws_lambda as _lambda,
    aws_apigateway as apigateway,
    aws_iam as iam,
    aws_logs as logs,
    Duration
)
from constructs import Construct

class ServerlessAiAgentRagStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # 1. Skapa en S3-bucket för din kunskapsbas (RAG)
        knowledge_base_bucket = s3.Bucket(
            self, "AiKnowledgeBaseBucket",
            removal_policy=RemovalPolicy.DESTROY, 
            auto_delete_objects=True,            
            encryption=s3.BucketEncryption.S3_MANAGED,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL 
        )

        # 2. Skapa din AI Backend Lambda-funktion
        ai_backend_lambda = _lambda.Function(
            self, "AiAgentBackendLambda",
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler="agent_backend.handler",
            code=_lambda.Code.from_asset("src"),
            timeout=Duration.seconds(30), # Ger Claude tid att generera svar
            memory_size=256,              
            log_retention=logs.RetentionDays.ONE_WEEK 
        )

        # 3. IAM-rättigheter för att anropa Amazon Bedrock (Least Privilege)
        ai_backend_lambda.add_to_role_policy(iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            actions=["bedrock:InvokeModel"],
            resources=[
                # Vi tillåter alla officiella Anthropic Claude-modeller samt dess europeiska profil-endpoints
                "arn:aws:bedrock:*::foundation-model/anthropic.claude-*",
                "arn:aws:bedrock:eu-north-1::inference-profile/*"
            ]
        ))

        # 4. Skapa en REST API Gateway för att exponera ditt AI-API
        api = apigateway.RestApi(
            self, "AiAgentRestApi",
            rest_api_name="Serverless AI Agent Service",
            description="Exposes an endpoint to converse with Amazon Bedrock Claude 3.",
            default_cors_preflight_options=apigateway.CorsOptions(
                allow_origins=apigateway.Cors.ALL_ORIGINS, 
                allow_methods=["POST", "OPTIONS"]
            )
        )

        # 5. Skapa en /ask-slutpunkt (Endpoint) som tar emot POST-anrop
        ask_resource = api.root.add_resource("ask")
        lambda_integration = apigateway.LambdaIntegration(ai_backend_lambda)
        ask_resource.add_method("POST", lambda_integration)
