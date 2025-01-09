from huggingface_hub import InferenceClient

class HuggingFaceAPIModel:
    def __init__(self, model_name: str = "google/flan-t5-large", api_token: str = "your-huggingface-api-token"):
        """
        Initializes the Hugging Face Inference API model.
        :param model_name: Name of the hosted model to use (default: google/flan-t5-large).
        :param api_token: Hugging Face API token.
        """
        self.client = InferenceClient(model=model_name, token=api_token)

    def query(self, prompt: str, max_length: int = 150) -> str:
        """
        Queries the Hugging Face Inference API using the new InferenceClient.
        :param prompt: Input prompt text.
        :param max_length: Maximum length of the generated response.
        :return: Generated response as a string.
        """
        try:
            response = self.client.text_generation(prompt, max_new_tokens=max_length)
            if response.startswith(prompt):  # Remove input prompt if included in output
                return response[len(prompt):].strip()
            return response.strip()
        except Exception as e:
            return f"Error: {e}"
