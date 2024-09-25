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


from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from measure.api.v1.measurement  import router as measurmentrouter
from measure.api.v1.catalogs  import router as catalogrouter
import requests

# Security setup
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="http://127.0.0.1:8001/api/v1/auth/login")

def verify_token(token: str):
    try:
        response = requests.post(
            "http://127.0.0.1:8001/api/v1/auth/verify-token",
            headers={"Authorization": f"Bearer {token}"}
        )
        if response.status_code != 200:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
        return response.json()["username"]
    except requests.RequestException:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")

# FastAPI app
app = FastAPI()

# Enable CORS
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

# Schemas
class Measurement(BaseModel):
    value: float
    unit: str

@app.post("/measurements/", response_model=Measurement)
def create_measurement(measurement: Measurement, token: str = Depends(oauth2_scheme)):
    username = verify_token(token)
    # Here, you would typically save the measurement to the database
    return measurement

@app.get("/measurements/public")
def get_public_measurements():
    # Public endpoint that returns some default data
    return {"data": "This is public measurement data"}

app.include_router(measurmentrouter)
app.include_router(catalogrouter)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
