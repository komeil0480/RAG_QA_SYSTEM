from models.hugging_face_model import HuggingFaceAPIModel

if __name__ == "__main__":
   
    api_token = ""

    # Initialize the Hugging Face API model
    hf_api_model = HuggingFaceAPIModel(model_name="google/flan-t5-large", api_token=api_token)

    # Test the model with a prompt
    prompt = "introduce your self"
    response = hf_api_model.query(prompt, max_length=100)
    print("Response from Hugging Face API Model:", response)
