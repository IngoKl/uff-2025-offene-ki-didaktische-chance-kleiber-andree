import openai
from openai import OpenAI


def generate(messages: dict, base_url: str = "https://api.openai.com/v1/", model: str = "gpt-4o") -> str:
    print(messages, model, base_url)

    client = OpenAI(base_url=base_url)

    messages.append({"role": "system", "content": "Du bist ein Chatbot, der immer im Kontext des University:Future Festivals 2025 antwortet."})

    try:
        completion = client.chat.completions.create(
            model=model,
            messages=messages,
        )
    except openai.ConflictError as e:
        return "Conflict error occurred."
    except openai.OpenAIError as e:
        return "OpenAI error occurred."

    return(completion.choices[0].message.content)