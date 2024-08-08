from haystack.components.embedders import SentenceTransformersTextEmbedder
from haystack_integrations.document_stores.elasticsearch import ElasticsearchDocumentStore
from haystack_integrations.components.retrievers.elasticsearch import ElasticsearchEmbeddingRetriever
from haystack import Pipeline
def get_retrieval_pipeline():
    INDEX= "medium-articles"
    HOST = "http://localhost:9200"
    document_store = ElasticsearchDocumentStore(index=INDEX,hosts=HOST)
    retrieval_pipeline = Pipeline()
    text_embedder = SentenceTransformersTextEmbedder()
    retrieval_pipeline.add_component("text_embedder", text_embedder)
    retrieval_pipeline.add_component(
        "retriever", ElasticsearchEmbeddingRetriever(document_store=document_store, top_k=10)
    )
    retrieval_pipeline.connect("text_embedder", "retriever")
    return retrieval_pipeline
