from elasticsearch import Elasticsearch, exceptions
from config import settings
from logger import logger, log_error_context
from caching import cache_data, retrieve_cache, invalidate_cache
import time
from cachetools import TTLCache, cached
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from agential import Agent

class DocumentRetrievalAgent(Agent):
    def __init__(self):
        self.es = Elasticsearch([settings.ELASTICSEARCH_URL])
        self.cache = TTLCache(maxsize=100, ttl=300)  # Cache with 100 items and 5 minutes TTL

    @cached(cache)
    @retry(stop=stop_after_attempt(5), wait=wait_exponential(), retry=retry_if_exception_type(exceptions.ConnectionError))
    def retrieve_documents(self, query):
        try:
            # Check if cached
            cached_docs = retrieve_cache(query)
            if cached_docs:
                return cached_docs

            response = self.es.search(
                index=settings.INDEX_NAME,
                body={
                    "query": {
                        "fuzzy": {
                            "content": {
                                "value": query,
                                "fuzziness": "AUTO"
                            }
                        }
                    }
                },
                size=10  # Retrieve top 10 documents for better performance
            )
            docs = [hit["_source"]["content"] for hit in response["hits"]["hits"]]

            # Cache the result
            cache_data(query, docs)

            return docs
        except exceptions.TransportError as e:
            log_error_context(e, "Transport error during document retrieval")
            raise
        except Exception as e:
            log_error_context(e, "Unexpected error during document retrieval")
            raise

    def refresh_index(self):
        try:
            # Logic to refresh the document index periodically
            invalidate_cache(self.cache)
        except Exception as e:
            log_error_context(e, "Error refreshing index")
            raise
