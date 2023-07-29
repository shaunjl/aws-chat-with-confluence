# 🛠️ this is still a work in progress 🛠️

# Overview
Use Embedded Vector Store and an LLM to chat with your confluence docs
Goal is to do everything in aws. If I'm successful, I will rename the repo

# Details
The overall structure will be inspired by [peterw/Chat-With-Github-Repo](https://github.com/peterw/Chat-with-Github-Repo)

1. Create an embedding vector store of the content in question
  - will try to use [langchain.embedddings.BedrockEmbeddings](https://github.com/langchain-ai/langchain/blob/13b4f465e2e67451549dc0662495ae07b3530659/libs/langchain/langchain/embeddings/bedrock.py#L10)
  - will try to use AWS OpenSearch (which is basically ElasticSearch), following the [recommendations of this guy](https://betterprogramming.pub/%EF%B8%8Fso-you-want-to-store-your-llm-data-aws-opensearch-to-the-rescue-f704a0f70558)
2. use the embedding vector store to get relevant texts from the store
  - Create an embedding of the question (also using [langchain.embedddings.BedrockEmbeddings](https://github.com/langchain-ai/langchain/blob/13b4f465e2e67451549dc0662495ae07b3530659/libs/langchain/langchain/embeddings/bedrock.py#L10))
  - Perform similarity search in the vector store using the question embedding to get relevant texts from the store
3. provide the llm with the received texts + question as a prompt to answer the question
  - will try to use Claude 2 (recetly [made available](https://press.aboutamazon.com/2023/7/aws-expands-amazon-bedrock-with-additional-foundation-models-new-model-provider-and-advanced-capability-to-help-customers-build-generative-ai-applications)) on [langchain.llms.Bedrock](https://github.com/langchain-ai/langchain/blob/13b4f465e2e67451549dc0662495ae07b3530659/libs/langchain/langchain/llms/bedrock.py#L51)
  - use [langchain.chains.RetrievalQA](https://github.com/langchain-ai/langchain/blob/13b4f465e2e67451549dc0662495ae07b3530659/libs/langchain/langchain/chains/retrieval_qa/base.py#L27)

## License

[MIT License](LICENSE)