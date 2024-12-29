from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from app.core.database import engine, Base

logger = logging.getLogger(__name__)

class BaseService:
    def __init__(self, settings, service_name: str):
        @asynccontextmanager
        async def lifespan(app: FastAPI):
            await self._configure_db()
            yield

        self.app = FastAPI(
            title=settings.PROJECT_NAME,
            version=settings.VERSION,
            openapi_url=f"{settings.API_V1_STR}/openapi.json",
            lifespan=lifespan
        )
        self.settings = settings
        self.service_name = service_name
        self._configure_middleware()
        self._configure_health_checks()

    async def _configure_db(self):
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    def _configure_middleware(self):
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    def _configure_health_checks(self):
        @self.app.get("/health")
        async def health_check():
            return {"status": "healthy", "service": self.service_name}
