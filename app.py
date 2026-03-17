from fastapi import FastAPI, Form, Request, HTTPException
from pydantic import BaseModel
from google import genai
from schemas import PromptRequest
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

client = genai.Client(api_key="AIzaSyCa2MPCu5_X7UrWj21Haw8xr3G2tbOTCYk")
templates = Jinja2Templates(directory="templates")

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})

@app.post("/generate")
async def generate_text(request: PromptRequest = Form(...)):
    try:
        response =  client.models.generate_content(
    model="gemini-3-flash-preview", contents=request.prompt
)
        """ response = await client.models.generate_content(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": request.prompt}]
        ) """

        return ({"message": response.text})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))









