import os
from dotenv import load_dotenv
from langchain.llms import HuggingFaceHub

load_dotenv()

def get_chat_response(user_input):
    hf_key = os.getenv("HUGGINGFACE_API_KEY")

    # Usamos Falcon-7B que responde bien en español
    llm = HuggingFaceHub(
        repo_id="tiiuae/falcon-7b-instruct",
        huggingfacehub_api_token=hf_key,
        model_kwargs={"temperature": 0.5, "max_new_tokens": 200}
    )

    # Prompt simple en español
    prompt = f"Respondé en español profesional y claro: {user_input}"

    return llm.invoke(prompt)
