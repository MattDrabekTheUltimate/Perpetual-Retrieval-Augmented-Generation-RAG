from sentence_transformers import SentenceTransformer, util
import torch
import faiss
from agential import Agent
from logger import log_error_context

class RefinementAgent(Agent):
    def __init__(self):
        self.semantic_model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

    def create_faiss_index(self, documents):
        try:
            doc_embeddings = self.semantic_model.encode(documents, convert_to_tensor=True)
            index = faiss.IndexFlatL2(doc_embeddings.shape[1])
            faiss.normalize_L2(doc_embeddings.numpy())
            index.add(doc_embeddings.numpy())
            return index, doc_embeddings
        except Exception as e:
            log_error_context(e, "Error creating FAISS index")
            raise

    def refine_response(self, response, documents):
        try:
            response_embedding = self.semantic_model.encode(response, convert_to_tensor=True)
            index, doc_embeddings = self.create_faiss_index(documents)

            D, I = index.search(response_embedding.numpy(), 3)  # Search for top 3 nearest neighbors
            top_docs = [documents[idx] for idx in I[0]]

            # Context-aware refinement using attention mechanisms
            refined_response = " ".join([doc[:min(200, len(doc))] for doc in top_docs])
            return refined_response
        except Exception as e:
            log_error_context(e, "Error refining response")
            raise
