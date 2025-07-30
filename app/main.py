from fastapi import FastAPI
from app.routes import router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="UWI FAQ Chatbot")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # or your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
