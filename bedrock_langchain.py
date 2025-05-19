#export BEDROCK_AWS_REGION="your-region-url"
#export BEDROCK_AWS_ACCESS_KEY_ID="your-access-key-id"
#export BEDROCK_AWS_SECRET_ACCESS_KEY="your-secret-access-key"
from typing import Any
from langchain_core.callbacks import AsyncCallbackHandler
from langchain_aws.llms.bedrock import BedrockLLM 
import json
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_core.language_models import LanguageModelInput



class BedrockAsyncCallbackHandler(AsyncCallbackHandler):
    # Async callback handler that can be used to handle callbacks from langchain.

    async def on_llm_error(self, error: BaseException, **kwargs: Any) -> Any:
        reason = kwargs.get("reason")
        if reason == "GUARDRAIL_INTERVENED":
            print(f"Guardrails: {kwargs}")

payload = {
    "anthropic_version": "bedrock-2023-05-31",
    "messages": [
        {
            "role": "user",
            "content": "Hi how are you today?"
        }
    ],
    "max_tokens": 100000,
    "temperature": 0.7,
    "top_k": 250,
    "top_p": 1
}


# Convert the native request to JSON.
request = json.dumps(payload)

#Guardrails for Amazon Bedrock with trace
llm = BedrockLLM(
    model="arn:aws:bedrock:us-east-1:497773883116:inference-profile/us.anthropic.claude-3-7-sonnet-20250219-v1:0",
    model_kwargs={},
    #guardrails={"id": "<Guardrail_ID>", "version": "<Version>", "trace": True},
    callbacks=[BedrockAsyncCallbackHandler()],
    provider="Anthropic",
    )

response = llm.invoke("Hello how are you",)


print(response)
