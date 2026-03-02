from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.auth import router as auth_router
from routes.invoices import router as invoices_router
from routes.logs import router as logs_router
from routes.metrics import router as metrics_router
from routes.users import router as users_router
from database import engine, Base
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:8080", "http://localhost:8081", "http://localhost:8082", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(auth_router)
app.include_router(invoices_router)
app.include_router(logs_router)
app.include_router(metrics_router)
app.include_router(users_router)

@app.get("/")
def read_root():
    return {"message": "Invoice Hub Backend API"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
