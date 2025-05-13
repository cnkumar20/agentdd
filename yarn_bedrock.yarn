import { Bedrock } from "@langchain/community/llms/bedrock";

const llm = new Bedrock({
  model: "anthropic.claude-v2",
  region: process.env.BEDROCK_AWS_REGION ?? "us-east-1",
  // endpointUrl: "custom.amazonaws.com",
  credentials: {
    accessKeyId: process.env.BEDROCK_AWS_ACCESS_KEY_ID,
    secretAccessKey: process.env.BEDROCK_AWS_SECRET_ACCESS_KEY,
  },
  temperature: 0,
  maxTokens: undefined,
  maxRetries: 2,
  // other params...
});
