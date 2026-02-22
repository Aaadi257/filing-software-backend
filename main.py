from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from backend.database import engine, Base
from backend.routers import masters, files, movements
import os
import sys

app = FastAPI(title="Filing Management System")

# Create tables
Base.metadata.create_all(bind=engine)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ API routes under /api
app.include_router(masters.router, prefix="/api")
app.include_router(files.router, prefix="/api")
app.include_router(movements.router, prefix="/api")

# Detect correct base path
if getattr(sys, "frozen", False):
    # Running inside PyInstaller bundle
    base_path = os.path.join(os.path.dirname(sys.executable), "_internal")
else:
    # Running in dev
    base_path = os.path.dirname(__file__)

frontend_path = os.path.join(base_path, "frontend_build")

print("Frontend path:", frontend_path)

# Serve React build
if os.path.exists(frontend_path):
    app.mount(
        "/",
        StaticFiles(directory=frontend_path, html=True),
        name="frontend",
    )
else:
    print("Frontend folder NOT FOUND at:", frontend_path)

# ✅ Run server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
