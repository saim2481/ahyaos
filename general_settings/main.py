# from fastapi import FastAPI
# from measure.api.v1.measure import router as measure_router
# from fastapi.middleware.cors import CORSMiddleware

# app = FastAPI()

# # CORS configuration
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Adjust this according to your needs
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# app.include_router(measure_router, prefix="/api/v1/measure")

# @app.get("/")
# async def root():
#     return {"message": "Welcome to the Measure Service"}


from fastapi import FastAPI
from general_settings.api.v1.general_settings import router as general_settings
from fastapi.middleware.cors import CORSMiddleware
import asyncio

app = FastAPI()

# Mount your API endpoints
app.include_router(general_settings, prefix="/api/v1/general_settings")

# FastAPI app
# app = FastAPI()

# # Enable CORS
# origins = [
#     "http://127.0.0.1:8001",
#     "http://localhost:8001"
# ]

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this according to your needs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# @app.get("/")
# async def root():
#     return {"message": "Welcome to the Measure Service"}

# if __name__ == "__main__":
#     asyncio.run(main())
