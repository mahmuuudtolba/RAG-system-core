from app.domain.entities.embedding import Embedding
from typing import List
from openai import OpenAI
from app.application.interfaces.embedding_service import IEmbeddingService
from app.domain.exceptions import EmbeddingError
class OpenAIEmbeddingService(IEmbeddingService):
    """OpenAI embedding serice """

    def __init__(self , model_name:str = "text-embedding-3-small"):
        self.model_name = model_name
        self.client = OpenAI()
        

    async def create_embedding(self, text: str) -> Embedding:
        response = self.client.embeddings.create(
            input= text , 
            model = self.model_name
        )
        vector =  response.data[0].embedding
        return Embedding(
            vector=vector , 
            model = self.model_name , 
            text=text
        )

    async def create_embeddings_batch(self ,texts:List[str]) -> List[Embedding]:
        """Create embedding for multiple texts"""
        response = self.client.embeddings.create(
            input=texts , 
            model = self.model_name
        )

        vectors = []

        for text in texts:
            try:
                response = self.client.embeddings.create(
                    input=text ,
                    model=self.model_name
                )

                vector = response.data[0].embedding    
                vectors.append(
                    Embedding(
                        vector=vector,
                        model= self.model_name,
                        text=text
                    )
                ) 

            except Exception :
                raise EmbeddingError 

        return vectors