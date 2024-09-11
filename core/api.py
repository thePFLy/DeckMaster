from fastapi import FastAPI
from core.system import System

trad = System().show_traduction

# Variables
app = FastAPI(
    title="ReDeck API v1",
    description=trad(key="redeck_desc"),
    debug=False
)
