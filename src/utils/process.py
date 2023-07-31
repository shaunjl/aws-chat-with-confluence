from langchain.document_loaders import ConfluenceLoader
from langchain.text_splitter import CharacterTextSplitter, TokenTextSplitter
from langchain.embeddings import BedrockEmbeddings, OpenAIEmbeddings
from langchain.vectorstores import OpenSearchVectorSearch

def load_docs(confluence_space_key, confluence_url, confluence_username, confluence_api_key):
    loader = ConfluenceLoader(
        url=confluence_url,
        username = confluence_username,
        api_key= confluence_api_key
    )
    return loader.load(
        space_key=confluence_space_key, 
        limit=100) # Maximum number of pages to retrieve per request, use max_pages to set Maximum number of pages to retrieve in total (defaults 1000)

def split_docs(documents):
    text_splitter = CharacterTextSplitter(chunk_size=100, chunk_overlap=0)
    texts = text_splitter.split_documents(documents)
    text_splitter = TokenTextSplitter(chunk_size=1000, chunk_overlap=10) # TODO - encoding_name??
    return text_splitter.split_documents(texts)

def get_embeddings_function(use_alt):
  if use_alt
    return OpenAIEmbeddings()
  return BedrockEmbeddings(
    credentials_profile_name="bedrock-admin", endpoint_url="custom_endpoint_url"
  )


def store_texts_as_embeddings(texts):
    # https://github.com/langchain-ai/langchain/blob/13b4f465e2e67451549dc0662495ae07b3530659/libs/langchain/langchain/embeddings/bedrock.py#L10
    embeddings = get_embeddings_function(use_alt=True)
    service = 'aoss' # must set the service as 'aoss'
    region = 'us-east-2'
    credentials = boto3.Session(aws_access_key_id='xxxxxx',aws_secret_access_key='xxxxx').get_credentials()
    awsauth = AWS4Auth('xxxxx', 'xxxxxx', region,service, session_token=credentials.token)

    # https://github.com/langchain-ai/langchain/blob/master/libs/langchain/langchain/vectorstores/opensearch_vector_search.py#L352
    """Run more texts through the embeddings and add to the vectorstore.

      Args:
          texts: Iterable of strings to add to the vectorstore.
          metadatas: Optional list of metadatas associated with the texts.
          ids: Optional list of ids to associate with the texts.
          bulk_size: Bulk API request count; Default: 500

      Returns:
          List of ids from adding the texts into the vectorstore.

      Optional Args:
          vector_field: Document field embeddings are stored in. Defaults to
          "vector_field".

          text_field: Document field the text of the document is stored in. Defaults
          to "text".
    """
    docsearch = OpenSearchVectorSearch.add_texts(
      docs,
      embeddings,
      opensearch_url="host url",
      http_auth=awsauth,
      timeout = 300,
      use_ssl = True,
      verify_certs = True,
      connection_class = RequestsHttpConnection,
      index_name="test-index-using-aoss",
      engine="faiss",
    )


def process(confluence_space_key, confluence_url, confluence_username, confluence_api_key)
    """
    TODO - describe
    """
    docs = load_docs(
      confluence_space_key,
      confluence_url,
      confluence_username,
      confluence_api_key
    )

    texts = split_docs(docs)

    store_texts_as_embeddings(texts)
