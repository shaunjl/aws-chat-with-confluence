# 🛠️ this is still a work in progress 🛠️

# Overview
Use Embedded Vector Store and an LLM to chat with your confluence docs
Goal is to do everything in aws. If it doesn't work, I'll rename it

# Details
The overall structure will be inspired by [peterw/Chat-With-Github-Repo](https://github.com/peterw/Chat-with-Github-Repo)

1. Create an embedding vector store of the content in question
  - will try to use [langchain.embedddings.BedrockEmbeddings](https://github.com/langchain-ai/langchain/blob/13b4f465e2e67451549dc0662495ae07b3530659/libs/langchain/langchain/embeddings/bedrock.py#L10)
  - will try to use AWS OpenSearch (which is basically ElasticSearch) via [langchain.vectorstores.OpenSearchVectorSearch](https://github.com/langchain-ai/langchain/blob/13b4f465e2e67451549dc0662495ae07b3530659/libs/langchain/langchain/vectorstores/opensearch_vector_search.py#L319), following these resources:
    - langchain's [docs on how to use it with Amazon OpenSearch Service Serverles](https://python.langchain.com/docs/integrations/vectorstores/opensearch#using-aoss-amazon-opensearch-service-serverless)
    - this [announcement from AWS](https://aws.amazon.com/blogs/big-data/introducing-the-vector-engine-for-amazon-opensearch-serverless-now-in-preview/), which also states that more info on how to use it via langchain is forthcoming.
    - the [recommendations of this guy](https://betterprogramming.pub/%EF%B8%8Fso-you-want-to-store-your-llm-data-aws-opensearch-to-the-rescue-f704a0f70558)
  - if that doesn't work (or in the meantime), I'll use [FAISS](https://github.com/langchain-ai/langchain/blob/13b4f465e2e67451549dc0662495ae07b3530659/libs/langchain/langchain/vectorstores/faiss.py#L49) to be able to keep it local (and so still only relying on AWS)
2. use the embedding vector store to get relevant texts from the store
  - Create an embedding of the question (also using [langchain.embedddings.BedrockEmbeddings](https://github.com/langchain-ai/langchain/blob/13b4f465e2e67451549dc0662495ae07b3530659/libs/langchain/langchain/embeddings/bedrock.py#L10))
  - Perform similarity search in the vector store using the question embedding to get relevant texts from the store
3. provide the llm with the received texts + question as a prompt to answer the question
  - will try to use Claude 2 (recetly [made available](https://press.aboutamazon.com/2023/7/aws-expands-amazon-bedrock-with-additional-foundation-models-new-model-provider-and-advanced-capability-to-help-customers-build-generative-ai-applications)) on [langchain.llms.Bedrock](https://github.com/langchain-ai/langchain/blob/13b4f465e2e67451549dc0662495ae07b3530659/libs/langchain/langchain/llms/bedrock.py#L51)
  - use [langchain.chains.RetrievalQA](https://github.com/langchain-ai/langchain/blob/13b4f465e2e67451549dc0662495ae07b3530659/libs/langchain/langchain/chains/retrieval_qa/base.py#L27)

## License

[MIT License](LICENSE)