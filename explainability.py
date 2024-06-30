import shap
import torch

class Explainability:
    def __init__(self, model, tokenizer):
        self.model = model
        self.tokenizer = tokenizer

    def explain(self, text):
        inputs = self.tokenizer(text, return_tensors='pt')
        explainer = shap.Explainer(self.model, inputs['input_ids'])
        shap_values = explainer.shap_values(inputs['input_ids'])
        shap.summary_plot(shap_values, inputs['input_ids'])
