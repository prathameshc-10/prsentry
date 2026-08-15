from fastapi import FastAPI
from dotenv import load_dotenv
from app.api.webhooks import router as webhook_router

load_dotenv()

app = FastAPI(title="PRSentry")
app.include_router(webhook_router)

@app.get("/health")
def health():
    return {"status": "ok"}