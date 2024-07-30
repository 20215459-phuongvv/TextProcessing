from fastapi import APIRouter
from api.v1.cluster import router as cluster_router

api_v1_router = APIRouter()
api_v1_router.include_router(cluster_router, prefix='/cluster', tags=["Clustering"])