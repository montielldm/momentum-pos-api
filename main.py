from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.auth.router import auth
from app.products.router import products
from app.tickets.router import tickets
from app.activities.router import activities

app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth)
app.include_router(tickets)
app.include_router(products)
app.include_router(activities)
