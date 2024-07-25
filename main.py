from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import ollama

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/chat", response_class=HTMLResponse)
async def chat(request: Request, message: str = Form(...)):
    # Use Ollama to generate a response
    response = ollama.chat(
        model="llama3.1:8b",
        messages=[
            {
                "role": "user",
                "content": message,
            },
        ],
    )

    ai_message = response["message"]["content"]

    return templates.TemplateResponse(
        "chat_messages.html",
        {"request": request, "ai_message": ai_message, "user_message": message},
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
