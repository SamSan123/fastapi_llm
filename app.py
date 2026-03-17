from fastapi import FastAPI, Form, Request, HTTPException
from pydantic import BaseModel
from google import genai
from schemas import PromptRequest
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import List

client = genai.Client(api_key="AIzaSyBqgvf7L-oI4I37IWcyDNiHZxftWfbKGEA")
templates = Jinja2Templates(directory="templates")

app = FastAPI()

#@app.get("/", response_class=HTMLResponse)
#def home(request: Request):
#    return templates.TemplateResponse("form.html", {"request": request})

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

# Blog model
class Blog(BaseModel):
    id: int
    title: str
    content: str



# In-memory storage for blogs
blogs: List[Blog] = []

@app.get("/")
def read_root():
    return {"message": "Welcome to the Blog API"}

@app.get("/blogs", response_model=List[Blog])
def get_blogs():
    return blogs

@app.get("/blogs/{blog_id}", response_model=Blog)
def get_blog(blog_id: int):
    for blog in blogs:
        if blog.id == blog_id:
            return blog
    raise HTTPException(status_code=404, detail="Blog not found")

@app.post("/blogs", response_model=Blog)
def create_blog(blog: Blog):
    for existing_blog in blogs:
        if existing_blog.id == blog.id:
            raise HTTPException(status_code=400, detail="Blog with this ID already exists")
    blogs.append(blog)
    return blog

@app.put("/blogs/{blog_id}", response_model=Blog)
def update_blog(blog_id: int, updated_blog: Blog):
    for index, blog in enumerate(blogs):
        if blog.id == blog_id:
            blogs[index] = updated_blog
            return updated_blog
    raise HTTPException(status_code=404, detail="Blog not found")

@app.get("/blogs/{blog_id}/display", response_class=HTMLResponse)
def display_blog(blog_id: int, request: Request):
    for blog in blogs:
        if blog.id == blog_id:
            return templates.TemplateResponse("blog_display.html", {"request": request, "blog": blog})
    raise HTTPException(status_code=404, detail="Blog not found")

@app.delete("/blogs/{blog_id}")
def delete_blog(blog_id: int):
    for index, blog in enumerate(blogs):
        if blog.id == blog_id:
            blogs.pop(index)
            return {"message": "Blog deleted successfully"}
    raise HTTPException(status_code=404, detail="Blog not found")







