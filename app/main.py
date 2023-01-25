from fastapi import FastAPI
from app.router import main_router
from app.database.dbbase import engine, Base

# Init DB
Base.metadata.create_all(bind=engine)

# Init API
app = FastAPI()

# Add routes
app.include_router(main_router.router)

