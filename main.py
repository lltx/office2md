from pathlib import Path
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi import HTTPException

from app.api.endpoints import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时执行
    current_dir = Path(__file__).parent
    banner_path = current_dir / 'app' / 'banner.txt'
    print(f"Looking for banner at: {banner_path.absolute()}")
    try:
        with open(banner_path, 'r', encoding='utf-8') as f:
            banner = f.read()
        print(banner)
    except FileNotFoundError:
        print(f"Banner file not found at {banner_path}, starting server without banner...")
    yield

def create_app() -> FastAPI:
    app = FastAPI(
        lifespan=lifespan
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 注册路由
    app.include_router(router)

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request, exc):
        return JSONResponse(
            status_code=exc.status_code,
            content={"message": exc.detail},
        )

    return app

app = create_app()