import os

from groq import Groq

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

"""
Example usage of Groq API to create a chat completion
This code snippet uses the Groq API to create a chat completion with a specific model and messages.
completion = client.chat.completions.create(
    model="meta-llama/llama-4-scout-17b-16e-instruct",
    messages=[
        {
            "role": "user",
            "content": "how can i integrate groq in fastapi and how to use it , give me a step by step guide\n"
        },
        {
            "role": "assistant",
            "content": "Groq is an AI model that provides fast and efficient inference capabilities, and FastAPI is a modern web framework for building APIs. Here's a step-by-step guide on how to integrate Groq with FastAPI:\n\n**Prerequisites**\n\n1. **Install FastAPI**: Run `pip install fastapi` in your terminal.\n2. **Install Groq**: Run `pip install groq` in your terminal.\n3. **Create a Groq account**: Sign up for a Groq account and obtain an API key.\n\n**Step 1: Set up Groq**\n\n1. Import the Groq library: `import groq`\n2. Initialize the Groq client with your API key: `client = groq.Groq(api_key=\"YOUR_API_KEY\")`\n\n**Step 2: Create a FastAPI App**\n\n1. Create a new file `main.py` and add the following code:\n```python\nfrom fastapi import FastAPI\napp = FastAPI()\n```\n**Step 3: Define a Groq Model**\n\n1. Choose a pre-trained Groq model that you want to use (e.g., `llama2-7b-chat`).\n2. Define a function that loads the model and sets up the Groq client:\n```python\nimport groq\n\ndef load_groq_model(model_name: str):\n    client = groq.Groq(api_key=\"YOUR_API_KEY\")\n    model = client.models.get(model_name)\n    return model\n```\n**Step 4: Create an API Endpoint**\n\n1. Create an API endpoint that accepts input data (e.g., text) and uses the Groq model to generate a response:\n```python\nfrom fastapi import FastAPI, Request\nfrom pydantic import BaseModel\n\napp = FastAPI()\n\nclass InputData(BaseModel):\n    text: str\n\n@app.post(\"/generate\")\nasync def generate_response(input_data: InputData):\n    model = load_groq_model(\"llama2-7b-chat\")\n    input_text = input_data.text\n    response = model.generate(input_text)\n    return {\"response\": response}\n```\n**Step 5: Run the FastAPI App**\n\n1. Run the FastAPI app using `uvicorn`: `uvicorn main:app --host 0.0.0.0 --port 8000`\n2. Open a tool like `curl` or a REST client (e.g., Postman) and send a POST request to `http://localhost:8000/generate` with a JSON body containing the input text:\n```json\n{\n  \"text\": \"Hello, how are you?\"\n}\n```\n**Step 6: Use the Groq Model**\n\n1. The FastAPI app will receive the input text, pass it through the Groq model, and return the generated response.\n\nHere's the complete code:\n```python\nfrom fastapi import FastAPI, Request\nfrom pydantic import BaseModel\nimport groq\n\napp = FastAPI()\n\nclass InputData(BaseModel):\n    text: str\n\ndef load_groq_model(model_name: str):\n    client = groq.Groq(api_key=\"YOUR_API_KEY\")\n    model = client.models.get(model_name)\n    return model\n\n@app.post(\"/generate\")\nasync def generate_response(input_data: InputData):\n    model = load_groq_model(\"llama2-7b-chat\")\n    input_text = input_data.text\n    response = model.generate(input_text)\n    return {\"response\": response}\n\nif __name__ == \"__main__\":\n    import uvicorn\n    uvicorn.run(app, host=\"0.0.0.0\", port=8000)\n```\nReplace `YOUR_API_KEY` with your actual Groq API key.\n\n**Example Use Cases**\n\n* Text generation: Use the `/generate` endpoint to generate text based on a given input prompt.\n* Chatbots: Integrate the Groq model with a chatbot framework to generate human-like responses to user input.\n\nNote that this is just a basic example to get you started. You may want to add error handling, implement authentication and authorization, and fine-tune the Groq model for your specific use case."
        },
        {
            "role": "user",
            "content": "which pre-trained groq model will be the best for a mental health app\nalso i am using a postgressql db, do i need to get all previous conversation and send it everytime i am making a request?\n"
        },
        {
            "role": "assistant",
            "content": "**Choosing a Pre-trained Groq Model for Mental Health App**\n\nFor a mental health app, you'll want to choose a model that's specifically designed for conversational dialogue and can understand the nuances of human emotions. Here are some pre-trained Groq models that might be suitable:\n\n1. **`llama2-7b-chat`**: A conversational model fine-tuned for chat-like interactions. It's a good starting point, but you may need to fine-tune it further for your specific use case.\n2. **`llama2-13b-chat`**: A larger version of the previous model, which might provide more detailed and empathetic responses.\n3. **`flan-20b`**: A more general-purpose model that's been fine-tuned on a large dataset of conversational text. It might be a good choice if you want a model that's more flexible and can handle a wide range of topics.\n\nConsider the following factors when choosing a model:\n\n* **Model size**: Larger models (e.g., `llama2-13b-chat`) might provide more detailed responses, but they also require more computational resources.\n* **Fine-tuning**: If you have a specific dataset or use case, you might want to fine-tune a model to better suit your needs.\n* **Conversational flow**: If you want a model that can engage in a more natural-sounding conversation, look for models that are specifically designed for chat-like interactions (e.g., `llama2-7b-chat`).\n\n**Using Previous Conversations with Groq**\n\nRegarding your second question, you don't necessarily need to send all previous conversations with every request. However, there are a few approaches you can take to leverage context from previous conversations:\n\n1. **Session-based conversations**: Store the conversation history in your PostgreSQL database and pass the relevant context to the Groq model with each request. This approach allows the model to understand the conversation flow and respond accordingly.\n2. **Contextual prompts**: Use a contextual prompt that includes a brief summary of the conversation history. This can help the model understand the context without requiring a large amount of text to be passed with each request.\n3. **Fine-tune the model**: Fine-tune the Groq model on your specific dataset, which includes conversation histories. This approach can help the model learn to understand the context and respond accordingly.\n\nTo implement session-based conversations, you can:\n\n1. Store the conversation history in your PostgreSQL database using a table with the following columns:\n\t* `conversation_id` (primary key)\n\t* `user_id` (foreign key referencing the user table)\n\t* `message` (the text of the message)\n\t* `timestamp` (the timestamp of the message)\n2. When a user sends a new message, retrieve the conversation history from the database and pass it to the Groq model along with the new message.\n3. Use the Groq model's response to update the conversation history in the database.\n\nHere's an example of how you could modify your FastAPI endpoint to use session-based conversations:\n```python\nfrom fastapi import FastAPI, Request\nfrom pydantic import BaseModel\nimport groq\nimport psycopg2\n\napp = FastAPI()\n\nclass InputData(BaseModel):\n text: str\n\n# Establish a connection to the PostgreSQL database\nconn = psycopg2.connect(\n host=\"your_host\",\n database=\"your_database\",\n user=\"your_username\",\n password=\"your_password\"\n)\n\n# Define a function to retrieve the conversation history\ndef get_conversation_history(conversation_id: int):\n cur = conn.cursor()\n cur.execute(\"SELECT message FROM conversation_history WHERE conversation_id = %s\", (conversation_id,))\n history = cur.fetchall()\n return [row[0] for row in history]\n\n# Define a function to update the conversation history\ndef update_conversation_history(conversation_id: int, message: str):\n cur = conn.cursor()\n cur.execute(\"INSERT INTO conversation_history (conversation_id, message) VALUES (%s, %s)\", (conversation_id, message))\n conn.commit()\n\n@app.post(\"/generate\")\nasync def generate_response(input_data: InputData, conversation_id: int):\n # Retrieve the conversation history\n history = get_conversation_history(conversation_id)\n\n # Pass the conversation history and new message to the Groq model\n model = load_groq_model(\"llama2-7b-chat\")\n input_text = \"\\n\".join(history + [input_data.text])\n response = model.generate(input_text)\n\n # Update the conversation history\n update_conversation_history(conversation_id, input_data.text)\n update_conversation_history(conversation_id, response)\n\n return {\"response\": response}\n```\nNote that this is just a basic example, and you'll likely need to modify it to fit your specific use case. Additionally, you may want to consider implementing techniques like conversation summarization or context pruning to reduce the amount of text being passed to the Groq model."
        },
        {
            "role": "user",
            "content": ""
        }
    ],
    temperature=1,
    max_completion_tokens=1024,
    top_p=1,
    stream=True,
    stop=None,
)

for chunk in completion:
    print(chunk.choices[0].delta.content or "", end="")
"""

async def get_groq_response(messages: list, model: str = "llama2-13b-chat", temperature: float = 1.0, max_tokens: int = 1024):
    """
    Asynchronous function to get chat completion from Groq API.
    """
    completion = await client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_completion_tokens=max_tokens,
        top_p=1,
        stream=True,
    )
    
    response = ""
    async for chunk in completion:
        response += chunk.choices[0].delta.content or ""
    
    return response