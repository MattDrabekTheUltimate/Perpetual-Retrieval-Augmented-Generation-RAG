from transformers import AutoModelForCausalLM, AutoTokenizer
from config import settings
from logger import logger, log_error_context
from agential import Agent

class ResponseGenerationAgent(Agent):
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained(settings.MODEL_NAME)
        self.model = AutoModelForCausalLM.from_pretrained(settings.MODEL_NAME)

    @track_inference_time
    def generate_response(self, prompt):
        try:
            inputs = self.tokenizer(prompt, return_tensors='pt')
            if len(inputs['input_ids'][0]) > self.tokenizer.model_max_length:
                logger.warning("Input prompt is too long, truncating...")
                inputs = self.tokenizer(prompt, return_tensors='pt', truncation=True, max_length=self.tokenizer.model_max_length)

            outputs = self.model.generate(**inputs, max_new_tokens=150)  # Limit the length of generated response
            return self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        except RuntimeError as e:
            if 'CUDA out of memory' in str(e):
                logger.error("CUDA out of memory. Consider reducing the batch size or model size.")
            log_error_context(e, "Runtime error during response generation")
            return ""
        except Exception as e:
            log_error_context(e, "Unexpected error during response generation")
            return ""

    def retrain_model(self):
        try:
            # Logic to retrain the generative model periodically
            pass
        except Exception as e:
            log_error_context(e, "Error retraining model")
            raise
