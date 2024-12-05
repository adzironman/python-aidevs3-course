import os
from datetime import datetime
from collections import defaultdict
import uuid

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

from src.clients.jina_embedding_client import JinaEmbeddingClient
from src.clients.openai_client import OpenAIClient
from src.services.audio_files_service import get_all_file_paths
from src.tasks.base_task import BaseTask


class EmbeddingTask(BaseTask):
    def __init__(self):
        super().__init__("wektory")
        self.enriched_docs = defaultdict(dict)
        self.ai_client = OpenAIClient()
        self.qdrant_client = QdrantClient(
            url=os.getenv("QDRANT_REMOTE_URL"),
            api_key=os.getenv("QDRANT_API_KEY"),
        )
        self.jina_embedding_client = JinaEmbeddingClient()


    def add_uuids(self):
        '''Adds UUID to each document.'''
        for key, documents in self.enriched_docs.items():
            self.logger.info(f"Adding UUID to file: {key}")
            documents["metadata"]["uuid"] = str(uuid.uuid4())
    

    def enrich_docs_with_basic_metadata(self):
        '''Enrichs docs with basic metadata.'''
        files_paths = get_all_file_paths(os.path.expanduser("~/Desktop/dev_materials/ai_devs3/pliki_z_fabryki/do-not-share/"))
        for file_path in files_paths:
            file_name = file_path.split("/")[-1]
                    
            # Skip non-text files
            if not file_name.endswith('.txt'):
                self.logger.info(f"Skipping non-text file: {file_name}")
                continue
            
            self.logger.info(f"Processing file and extracting basic metadata: {file_name}")

            with open(file_path, "r") as f:
                text = f.read()
                self.enriched_docs[file_name]["metadata"] ={
                    "file_name": file_name,
                    "date": datetime.strptime(file_name.split(".")[0], "%Y_%m_%d").date().strftime("%Y-%m-%d"),
                    "length": len(text),
                }
            self.enriched_docs[file_name]["content"] = text
    
    def extract_main_topic_using_llm(self, text: str):
        '''
        Extracts main topic from the text using LLM.
        '''
        sys_prompt = f"""
        <instrukcje>
        W tekście przesłanym przez użytkownika jest zawarta nazwa urządzania militarnego.
        Wyselekcjonuj z tekstu słowa kluczowe.
        Zwracaj uwagę przede wszystkim na nazwy własne, nazwy urządzeń, nazwy miejsc, nazwy jednostek organizacyjnych, zdarzenia, czynności.
        Zamień każde słowo kluczowe na formę podstawową.
        Zwróć słowa kluczowe w postaci listy oddzielonej przecinkami. Nie stosuj żadnego innego formatowania.
        </instrukcje>
        """
        ai_response = self.ai_client.answer_question(system_message=sys_prompt, question=text, response_format="text")
        return ai_response
    
    def enrich_docs_with_main_topic(self):
        '''Enrichs docs with main topic.'''
        for key, documents in self.enriched_docs.items():
            documents["metadata"]["main_topic"] = self.extract_main_topic_using_llm(documents["content"])

    def embed_docs_into_qdrant(self):
        '''Embeds docs into Qdrant.'''

        docs = [
            document["content"]
            for _, document in self.enriched_docs.items()
        ]
        meta = [
            {
                "date": document["metadata"]["date"],
                "length": document["metadata"]["length"],
                "main_topic": document["metadata"]["main_topic"]
            }
            for _, document in self.enriched_docs.items()
        ]

        ids = [
            document["metadata"]["uuid"]
            for _, document in self.enriched_docs.items()
        ]

        self.qdrant_client.add(
            collection_name="s03e02",
            documents=docs,
            metadata=meta,
            ids=ids
        )

        self.qdrant_client.ups


    #This solution using default embedding model from Qdrant does not work well.
    # def process(self):
    #     self.enrich_docs_with_basic_metadata()
    #     self.add_uuids()
    #     self.enrich_docs_with_main_topic()

    #     self.embed_docs_into_qdrant()


    #     search_result = self.qdrant_client.query(
    #         collection_name="s03e02",
    #         query_text="w raporcie z którego dnia znajduje się wzmianka o kradzieży prototypu broni?",
    #         limit=20
    #     )

    #     for res in search_result:
    #         print(f"Date: {res.metadata['date']}, score: {res.score}, main_topic: {res.metadata['main_topic']}")
        
    #     return search_result[0].metadata['date']
    

    def embed_docs_into_qdrant_using_jina(self, collection_name: str):
        '''Embeds docs into Qdrant using Jina.'''

        for key, document in self.enriched_docs.items():
            document["metadata"]["embedding"] = self.jina_embedding_client.create_jina_embedding(document["content"])


        self.qdrant_client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=1024, distance=Distance.COSINE)
        )
        points = [
            PointStruct(
                id=document["metadata"]["uuid"],
                vector=document["metadata"]["embedding"],
                payload={
                    "doc": document["content"],
                    "date": document["metadata"]["date"],
                    "main_topic": document["metadata"]["main_topic"]
            }
        )
            for _, document in self.enriched_docs.items()
        ]

        self.qdrant_client.upsert(
            collection_name=collection_name,
            points=points
        )

    def process(self):
        collection_name = "s03e02_Jina"
        self.enrich_docs_with_basic_metadata()
        self.add_uuids()
        self.enrich_docs_with_main_topic()

        self.embed_docs_into_qdrant_using_jina(collection_name)


        query = "W raporcie, z którego dnia znajduje się wzmianka o kradzieży prototypu broni?"
        search_result = self.qdrant_client.search(
            collection_name=collection_name,
            query_vector=self.jina_embedding_client.create_jina_embedding(query),
            limit=1
        )

        answer = search_result[0].payload["date"]
        print(answer)
        return answer






    


