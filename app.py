import uvicorn
import os
import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.v1 import api_v1_router
from config.env import ENV
from api.middleware.error_handler import return_error

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
env = ENV()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_v1_router, prefix='/api/v1')

@app.get("/")
def hello_world():
    return 'Hello World!'

@app.exception_handler(Exception)
def validation_exception_handler(request, err):
    return return_error(request, err)


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=ENV.PORT)
