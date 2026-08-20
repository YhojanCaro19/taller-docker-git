from fastapi import FastAPI
import os

app = FastAPI(title="App CI/CD (ejercicio)")


@app.get("/")
def index():
    return {
        "mensaje": "Hola desde Docker + CI/CD! (ejercicio - FastAPI)",
        "version": os.environ.get("APP_VERSION", "1.0.0"),
        "entorno": os.environ.get("ENTORNO", "development"),
    }


@app.get("/health")
def health():
    return {"status": "healthy"}
