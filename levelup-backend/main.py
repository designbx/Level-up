from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.database import engine, Base
from routers import auth, leads, admin, contact

# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="LevelUp SMMA API",
    description="Backend API for LevelUp Social Media Marketing Agency",
    version="1.0.0"
)

# CORS — allow your frontend domain
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with your domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth.router,    prefix="/api/auth",    tags=["Auth"])
app.include_router(leads.router,   prefix="/api/leads",   tags=["Leads"])
app.include_router(contact.router, prefix="/api/contact", tags=["Contact"])
app.include_router(admin.router,   prefix="/api/admin",   tags=["Admin"])

@app.get("/")
def root():
    return {"message": "LevelUp API is running 🚀"}
