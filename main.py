from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routers import masters, files, movements

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Filing Management System")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(masters.router)
app.include_router(files.router)
app.include_router(movements.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Filing Management System API"}
