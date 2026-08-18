from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from app.api.webhooks import router as webhook_router

app = FastAPI(title="PRSentry")
app.include_router(webhook_router)

@app.get("/health")
def health():
    return {"status": "ok"}