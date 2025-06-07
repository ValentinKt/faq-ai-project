from typing import Dict, List
from uuid import UUID
from config.settings import settings
from sentence_transformers import SentenceTransformer
import qdrant_client
from qdrant_client.http import models as rest
from ollama import Client
import logging
from typing import List, Dict
from concurrent.futures import as_completed
import numpy as np

logger = logging.getLogger(__name__)

class AIService:
    """Handles AI-powered FAQ generation and document embedding."""

    def __init__(self):
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
        self.qdrant = qdrant_client.QdrantClient(settings.QDRANT_URL)
        self.ollama = Client(host=settings.OLLAMA_BASE_URL)

    def generate_faq(self, query: str, document_ids: List[UUID] = None) -> Dict:
        """Generate an FAQ answer using RAG."""
        try:
            query_embedding = self.embedder.encode(query).tolist()
            filter_condition = None
            if document_ids:
                filter_condition = rest.Filter(
                    must=[
                        rest.FieldCondition(
                            key="document_id",
                            match=rest.MatchValue(value=str(did))
                        ) for did in document_ids
                    ]
                )

            search_results = self.qdrant.search(
                collection_name="document_embeddings",
                query_vector=query_embedding,
                limit=5,
                query_filter=filter_condition
            )

            context = "\n\n".join([hit.payload.get('text', '') for hit in search_results])
            prompt = f"Question: {query}\nContext: {context}\nAnswer:"
            response = self.ollama.generate(model='mistral', prompt=prompt, options={"temperature": 0.3})

            return {
                "answer": response['response'],
                "confidence": min(max(response.get('confidence', 0.8), 0), 1),
                "sources": [hit.payload.get('document_id') for hit in search_results if 'document_id' in hit.payload]
            }
        except Exception as e:
            logger.exception("Error generating FAQ")
            raise

    def store_document_embedding(self, document_id: UUID, text: str) -> None:
        """Store document embedding in Qdrant."""
        try:
            embedding = self.embedder.encode(text).tolist()
            self.qdrant.upsert(
                collection_name="document_embeddings",
                points=[
                    rest.PointStruct(
                        id=str(document_id),
                        vector=embedding,
                        payload={"document_id": str(document_id), "text": text}
                    )
                ]
            )
            logger.info(f"Stored embedding for document: {document_id}")
        except Exception as e:
            logger.exception(f"Failed to store embedding for document {document_id}")
            raise
    
    async def process_documents_batch(self, documents: List[Dict]) -> None:
        """Process multiple documents in a single batch for efficiency."""
        if not documents:
            return

        try:
            logger.info(f"Processing batch of {len(documents)} documents")
            
            # Extract texts for embedding
            texts = [doc['text'] for doc in documents]
            
            # Batch embed documents
            embeddings = await self._executor.submit(
                self.embedder.encode, 
                texts,
                batch_size=32,
                convert_to_numpy=True
            )
            
            # Prepare points for Qdrant
            points = []
            for doc, embedding in zip(documents, embeddings):
                points.append(rest.PointStruct(
                    id=str(doc['id']),
                    vector=embedding.tolist(),
                    payload={
                        "document_id": str(doc['id']),
                        "text": doc['text'],
                        "metadata": doc.get('metadata', {})
                    }
                ))
            
            # Batch upsert to Qdrant
            await self._executor.submit(
                self.qdrant.upsert,
                collection_name="document_embeddings",
                points=points,
                wait=True
            )
            
            logger.info(f"Successfully processed {len(documents)} documents")
            
        except Exception as e:
            logger.error(f"Batch document processing failed: {str(e)}")
            raise APIError("Failed to process documents batch", 500)

    # Update the single document method to use batch internally
    def store_document_embedding(self, document_id: UUID, text: str) -> None:
        """Wrapper for single document processing using batch."""
        return self.process_documents_batch([{
            'id': document_id,
            'text': text
        }])