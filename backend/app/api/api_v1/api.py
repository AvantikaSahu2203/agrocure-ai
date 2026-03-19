from fastapi import APIRouter

from app.api.api_v1.endpoints import login, users, crops, disease, weather, admin, stores, maps, disease_detection, ecommerce, orchestrator, diseases, reports, market, advisory

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(crops.router, prefix="/crops", tags=["crops"])
api_router.include_router(disease.router, prefix="/disease", tags=["disease"])
api_router.include_router(disease_detection.router, prefix="/disease-ai", tags=["disease-ai"])
api_router.include_router(weather.router, prefix="/weather", tags=["weather"])
api_router.include_router(admin.router, prefix="/admin", tags=["admin"])
api_router.include_router(stores.router, prefix="/stores", tags=["stores"])
api_router.include_router(maps.router, prefix="/maps", tags=["maps"])
api_router.include_router(ecommerce.router, prefix="/ecommerce", tags=["ecommerce"])
api_router.include_router(orchestrator.router, prefix="/orchestrator", tags=["orchestrator"])
api_router.include_router(diseases.router, prefix="/diseases", tags=["diseases"])
api_router.include_router(reports.router, prefix="/reports", tags=["reports"])
api_router.include_router(market.router, prefix="/market", tags=["market"])
api_router.include_router(advisory.router, prefix="/advisory", tags=["advisory"])
