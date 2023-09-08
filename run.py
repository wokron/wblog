import uvicorn

from app import main

if __name__ == "__main__":
    uvicorn.run(app="app.main:app", reload=True)
