from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get('/')
def render_homepage():
    content = {'response': 'Welcome to Hoempage' }
    return JSONResponse(content= content, status_code=200)

