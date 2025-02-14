from fastapi import FastAPI, HTTPException
import openai

app = FastAPI()

# OpenAI API Key (Replace with a valid key)
openai.api_key = "your-openai-api-key"

@app.post("/generate")
async def generate_ai_response(request: dict):
    user_prompt = request.get("prompt", "Explain how AI improves workflow automation in business.")

    try:
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": user_prompt}]
        )
        ai_output = response.choices[0].message.content
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI API Error: {e}")

    return {"input": user_prompt, "output": ai_output}
