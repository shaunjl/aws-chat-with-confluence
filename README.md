# 🛠️ WIP 🛠️
This is currently a Work in Progress, it is basically an implementation plan.

To see a working version that uses OpenAI and open source, see [chat-with-confluence](https://github.com/shaunjl/chat-with-confluence)

# Overview
The intention of this repo is to use Embedded Vector Store and an LLM to chat with your confluence docs while assuming that you only have
an AWS license - no OpenAI, no other vector store service, nothing else.

# Details

## Approach (assuming you don't have access to Amazon Bedrock)
1. Create an embedding vector store of the Confluence docs
  - use [langchain.document_loaders.ConfluenceLoader](https://github.com/langchain-ai/langchain/blob/13b4f465e2e67451549dc0662495ae07b3530659/libs/langchain/langchain/document_loaders/confluence.py#L35) to load the Confluence docs
  - use [langchain.text_splitter.CharacterTextSplitter](https://github.com/langchain-ai/langchain/blob/c2d1d903fa35b91018b4d777db2b008fcbaa9fbc/langchain/text_splitter.py#L159) and [langchain.text_splitter.TokenTextSplitter](https://github.com/langchain-ai/langchain/blob/c2d1d903fa35b91018b4d777db2b008fcbaa9fbc/langchain/text_splitter.py#L177) to break up the docs into `documents` for processing
  - use HuggingFace sentance transformers embeddings
  - use postgres/pg_vector in RDS as the vector store
2. use the embedding vector store to get relevant texts from the store
  - Create an embedding of the question (also using HuggingFace)
  - Perform similarity search in the vector store using the question embedding to get relevant texts from the store
3. provide the llm with the received texts + question as a prompt to answer the question
  - Use llama-2, which is available in AWS Sagemaker
  - use [langchain.chains.RetrievalQA](https://github.com/langchain-ai/langchain/blob/13b4f465e2e67451549dc0662495ae07b3530659/libs/langchain/langchain/chains/retrieval_qa/base.py#L27)

## Alternative Approach assuming you have access to Bedrock 🪨

Amazon Bedrock is under "Limited Beta Preview" and it's super hard to get into the beta. I suspect this soution would be better. Here is how I _would_ do it. The main differences are bolded

1. Create an embedding vector store of the Confluence docs
  - use [langchain.document_loaders.ConfluenceLoader](https://github.com/langchain-ai/langchain/blob/13b4f465e2e67451549dc0662495ae07b3530659/libs/langchain/langchain/document_loaders/confluence.py#L35) to load the Confluence docs
  - use [langchain.text_splitter.CharacterTextSplitter](https://github.com/langchain-ai/langchain/blob/c2d1d903fa35b91018b4d777db2b008fcbaa9fbc/langchain/text_splitter.py#L159) and [langchain.text_splitter.TokenTextSplitter](https://github.com/langchain-ai/langchain/blob/c2d1d903fa35b91018b4d777db2b008fcbaa9fbc/langchain/text_splitter.py#L177) to break up the docs into `documents` for processing
  - **(different)** use [langchain.embedddings.BedrockEmbeddings](https://github.com/langchain-ai/langchain/blob/13b4f465e2e67451549dc0662495ae07b3530659/libs/langchain/langchain/embeddings/bedrock.py#L10)
  - **(different)** use AWS OpenSearch (which is basically ElasticSearch) via [langchain.vectorstores.OpenSearchVectorSearch](https://github.com/langchain-ai/langchain/blob/13b4f465e2e67451549dc0662495ae07b3530659/libs/langchain/langchain/vectorstores/opensearch_vector_search.py#L319) as a vector store, following these resources:
    - langchain's [docs on how to use it with Amazon OpenSearch Service Serverles](https://python.langchain.com/docs/integrations/vectorstores/opensearch#using-aoss-amazon-opensearch-service-serverless)
    - this [announcement from AWS](https://aws.amazon.com/blogs/big-data/introducing-the-vector-engine-for-amazon-opensearch-serverless-now-in-preview/), which also states that more info on how to use it via langchain is forthcoming.
    - the [recommendations of this guy](https://betterprogramming.pub/%EF%B8%8Fso-you-want-to-store-your-llm-data-aws-opensearch-to-the-rescue-f704a0f70558)
2. use the embedding vector store to get relevant texts from the store
  -  **(different)** Create an embedding of the question (also using [langchain.embedddings.BedrockEmbeddings](https://github.com/langchain-ai/langchain/blob/13b4f465e2e67451549dc0662495ae07b3530659/libs/langchain/langchain/embeddings/bedrock.py#L10))
  - Perform similarity search in the vector store using the question embedding to get relevant texts from the store
3. provide the llm with the received texts + question as a prompt to answer the question
  -  **(different)** use Claude 2 (recetly [made available](https://press.aboutamazon.com/2023/7/aws-expands-amazon-bedrock-with-additional-foundation-models-new-model-provider-and-advanced-capability-to-help-customers-build-generative-ai-applications)) on [langchain.llms.Bedrock](https://github.com/langchain-ai/langchain/blob/13b4f465e2e67451549dc0662495ae07b3530659/libs/langchain/langchain/llms/bedrock.py#L51)
  - use [langchain.chains.RetrievalQA](https://github.com/langchain-ai/langchain/blob/13b4f465e2e67451549dc0662495ae07b3530659/libs/langchain/langchain/chains/retrieval_qa/base.py#L27)

## License

[MIT License](LICENSE)