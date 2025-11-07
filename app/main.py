from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session
from .database import init_db
import app.database as database

# Routers
from .routes import menu_routes, category_routes, customer_routes, order_routes, addon_routes, payment_routes, auth

app = FastAPI(title="3awan Cafe & Resto API")

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_session():
    eng = database.engine
    if eng is None:
        raise RuntimeError("Database engine is not configured. Set DATABASE_URL or call database.set_engine().")
    with Session(eng) as session:
        yield session

@app.on_event("startup")
def on_startup():
    init_db()

# Include routers with prefix
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(category_routes.router, prefix="/api")
app.include_router(menu_routes.router, prefix="/api")
app.include_router(addon_routes.router, prefix="/api")
app.include_router(customer_routes.router, prefix="/api")
app.include_router(order_routes.router, prefix="/api")
app.include_router(payment_routes.router, prefix="/api")
