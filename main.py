from fastapi import FastAPI
from core.cors import CORSConfig

app = FastAPI(title="Vicio API")

CORSConfig.setup(app)
