from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {
        "message" : "Income Management API is running"
    }