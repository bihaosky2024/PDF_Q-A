from langchain_openai import ChatOpenAI
from langchain.chat_models import init_chat_model
from langchain_openai import OpenAIEmbeddings


def init_openai_model(api_key, model_name="gpt-4o-mini"):

    model = ChatOpenAI(model=model_name,
                       openai_api_key=api_key,
                       openai_api_base="https://api.aigc369.com/v1")
    return model
    
def init_ds_model(api_key, model_name="deepseek-chat"):

    model = init_chat_model(model=model_name,
                            model_provider="deepseek",
                            api_key=api_key,
                            base_url="https://api.deepseek.com")
    return model

def init_embedding_model(api_key, model_name="text-embedding-3-large"):

    model = OpenAIEmbeddings(model=model_name,
                             openai_api_key=api_key,
                             openai_api_base="https://api.aigc369.com/v1")
    return model