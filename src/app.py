import time
import uvicorn

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from .api.v1.router import userRouter, cabinetRouter, authRouter
from core.exceptions import (
    CoreException,
    ErrorDetail,
    ErrorLink,
    ErrorResponse,
)

app = FastAPI()

@app.exception_handler(CoreException)
async def core_exception_handler(request: Request, exc: CoreException):
    error_link = exc.links
    if error_link is None:
        error_link = ErrorLink(about="Not available", error_type="Undocumented")

    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            status=exc.status_code,
            detail=ErrorDetail(
                title="No title" if exc.title is None else exc.title,
                message=exc.message,
            ),
            links=error_link,
        ).dict(),
    )


app.include_router(userRouter)
app.include_router(cabinetRouter)
app.include_router(authRouter)

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return "hello"


def main():
    uvicorn.run("src.app:app", host="0.0.0.0", port=8000, reload=True)
