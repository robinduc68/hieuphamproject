import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse

from app.config import get_settings
from app.database import db
from app.routers.products       import router as products_router, cat_router, sub_router
from app.routers.collections    import router as collections_router
from app.routers.users          import router as users_router
from app.routers.orders         import router as orders_router, nl_router
from app.routers.admin          import router as admin_router
from app.routers.customization  import router as customization_router
from app.routers.uploads        import router as uploads_router
from app.routers.settings       import router as settings_router
from app.routers.posts          import router as posts_router

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Connect DB on startup
    if db.is_closed():
        db.connect(reuse_if_open=True)
    yield
    # Close DB on shutdown
    if not db.is_closed():
        db.close()


app = FastAPI(
    title="HUY VO API",
    description="Backend API cho trang web thương mại điện tử HUY VO – Vietnam's Sustainable Luxury House",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    lifespan=lifespan,
)

# ── CORS ──────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Static / Media files ──────────────────────────────────────────────────
os.makedirs(settings.media_dir, exist_ok=True)
app.mount("/media", StaticFiles(directory=settings.media_dir), name="media")

# ── Routers ───────────────────────────────────────────────────────────────
app.include_router(cat_router)
app.include_router(sub_router)
app.include_router(products_router)
app.include_router(collections_router)
app.include_router(users_router)
app.include_router(orders_router)
app.include_router(nl_router)
app.include_router(admin_router)
app.include_router(customization_router)
app.include_router(uploads_router)
app.include_router(settings_router)
app.include_router(posts_router)


# ── Health check ──────────────────────────────────────────────────────────
@app.get("/api/health", tags=["Health"])
def health():
    try:
        db.execute_sql("SELECT 1")
        db_status = "ok"
    except Exception as e:
        db_status = str(e)
    return {"status": "ok", "database": db_status, "version": "1.0.0"}


# ── Global exception handler ──────────────────────────────────────────────
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    if settings.debug:
        raise exc
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})
