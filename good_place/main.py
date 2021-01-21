"""
Entry point for good_place
"""
# pylint: disable=missing-function-docstring

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from good_place.apis.v1 import api_router
from good_place.core.settings import CONFIG
from good_place.db.utils import init_db

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=CONFIG.get("CORS_ORIGIN"),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", include_in_schema=False)
async def root():
    """
    Root redirect to api doc
    """
    return RedirectResponse(url="/docs")


@app.on_event("startup")
async def startup_event():
    print("Starting up...")
    init_db(app)


@app.on_event("shutdown")
async def shutdown_event():
    print("Shutting down...")


app.include_router(api_router, prefix=CONFIG.get("API_V1_STR"))

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
