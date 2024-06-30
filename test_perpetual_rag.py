import pytest
from unittest.mock import patch
from retrieval import DocumentRetrievalAgent
from generation import ResponseGenerationAgent
from refine import RefinementAgent
from validate import ValidationAgent

def test_retrieve_documents():
    with patch('retrieval.es.search') as mock_search:
        mock_search.return_value = {
            "hits": {
                "hits": [
                    {"_source": {"content": "Einstein's theory of relativity"}}
                ]
            }
        }
        retrieval_agent = DocumentRetrievalAgent()
        docs = retrieval_agent.retrieve_documents("Einstein")
        assert isinstance(docs, list)
        assert len(docs) > 0

def test_generate_response():
    with patch('generation.tokenizer') as mock_tokenizer, patch('generation.model') as mock_model:
        mock_tokenizer.return_tensors = lambda x, return_tensors: {"input_ids": [[1, 2, 3]]}
        mock_model.generate.return_value = [[4, 5, 6]]
        mock_tokenizer.decode.return_value = "Response"
        
        generation_agent = ResponseGenerationAgent()
        response = generation_agent.generate_response("What is AI?")
        assert isinstance(response, str)
        assert response == "Response"

def test_refine_response():
    refinement_agent = RefinementAgent()
    response = "AI is fascinating."
    docs = ["AI is fascinating and complex.", "AI has many applications."]
    refined = refinement_agent.refine_response(response, docs)
    assert any(doc in refined for doc in docs)

def test_validate_response():
    validation_agent = ValidationAgent()
    response = "AI is fascinating."
    docs = ["AI is fascinating and complex.", "AI has many applications."]
    is_valid = validation_agent.validate_response(response, docs)
    assert is_valid

if __name__ == "__main__":
    pytest.main()
