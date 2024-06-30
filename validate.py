from sentence_transformers import SentenceTransformer, util
import torch
from agential import Agent
from logger import log_error_context

class ValidationAgent(Agent):
    def __init__(self):
        self.semantic_model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

    def validate_response(self, response, documents):
        try:
            response_embedding = self.semantic_model.encode(response, convert_to_tensor=True)
            doc_embeddings = self.semantic_model.encode(documents, convert_to_tensor=True)
            similarities = util.pytorch_cos_sim(response_embedding, doc_embeddings)

            # Dynamic validation thresholds based on context
            threshold = 0.8  # Placeholder for dynamic threshold calculation
            if torch.any(similarities > threshold):
                return True
            return False
        except Exception as e:
            log_error_context(e, "Error during response validation")
            raise
