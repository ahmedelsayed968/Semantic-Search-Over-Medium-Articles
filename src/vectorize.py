from haystack_integrations.document_stores.elasticsearch import ElasticsearchDocumentStore
from haystack.components.writers import DocumentWriter

from haystack import Pipeline,Document
from haystack.components.preprocessors import DocumentCleaner, DocumentSplitter
from haystack.components.embedders import SentenceTransformersDocumentEmbedder
from haystack.components.writers import DocumentWriter
from haystack.document_stores.types import DuplicatePolicy
from haystack.utils import ComponentDevice
from tqdm import tqdm
import pandas as pd
def create_indexing_pipeline(document_store, metadata_fields_to_embed=None):
    document_cleaner = DocumentCleaner()
    # document_splitter = DocumentSplitter(split_by="sentence", split_length=2)
    document_embedder = SentenceTransformersDocumentEmbedder(
        meta_fields_to_embed=metadata_fields_to_embed
    )
    document_writer = DocumentWriter(document_store=document_store,
                                      policy=DuplicatePolicy.SKIP)

    indexing_pipeline = Pipeline()
    indexing_pipeline.add_component("cleaner", document_cleaner)
    # indexing_pipeline.add_component("splitter", document_splitter)
    indexing_pipeline.add_component("embedder", document_embedder)
    indexing_pipeline.add_component("writer", document_writer)

    indexing_pipeline.connect("cleaner", "embedder")
    # indexing_pipeline.connect("splitter", "embedder")
    indexing_pipeline.connect("embedder", "writer")

    return indexing_pipeline

def serialize_pipeline(pipeline,filename):
    string = index_pip.dumps()
    with open(f"pipelines/{filename}.yml",mode="w") as f:
        f.write(string)

class DataLoader:
    chunk_size = 2**20
    def __init__(self,path) -> None:
        self.path = path
    def read(self,limit=100):
        df = pd.read_csv(self.path)[:limit]
        docs = []

        for index,row in tqdm(df.iterrows(),desc="Converting to Documents",total=df.shape[0]):
            data = row.to_dict()
            docs.append(Document(content=data['text'],
                                id=index,
                                meta={"title":data['title'],
                                    "url":data['url'],
                                    "authors":data['authors'],
                                    "timestamp":data['timestamp'],
                                    "tags":data['tags']}))
        return docs
if __name__ == "__main__":
    chunk_size = 2**20 *10
    docs_articles = DataLoader(path="data/train.csv").read()

    INDEX= "medium-articles"
    HOST = "http://localhost:9200"
    document_store = ElasticsearchDocumentStore(index=INDEX,hosts=HOST)
    index_pip = create_indexing_pipeline(document_store=document_store,metadata_fields_to_embed=['title'])
    index_pip.draw("pipelines/indexing_pipeline.png")
    serialize_pipeline(index_pip,"index")
    index_pip.run({"cleaner":{"documents":docs_articles}})

