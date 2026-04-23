import openai
from app.config import get_settings

settings = get_settings()

openai_client = openai.AsyncOpenAI(api_key=settings.OPENAI_API_KEY)


async def generate_completion(
    system_prompt: str,
    user_prompt: str,
    model: str = None,
    temperature: float = 0.7,
    max_tokens: int = 2000,
    json_mode: bool = False,
) -> str:
    """Generate a completion using OpenAI."""
    model = model or settings.OPENAI_MODEL
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]
    
    kwargs = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    
    if json_mode:
        kwargs["response_format"] = {"type": "json_object"}
    
    response = await openai_client.chat.completions.create(**kwargs)
    return response.choices[0].message.content


async def generate_embedding(text: str, model: str = None) -> list:
    """Generate an embedding for the given text."""
    model = model or settings.OPENAI_EMBEDDING_MODEL
    response = await openai_client.embeddings.create(
        model=model,
        input=text,
    )
    return response.data[0].embedding
