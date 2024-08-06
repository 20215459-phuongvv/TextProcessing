from fastapi import APIRouter
from api.v1.cluster import router as cluster_router
from api.v1.summarize import router as summarize_router

api_v1_router = APIRouter()
api_v1_router.include_router(cluster_router, prefix='/cluster', tags=["Clustering"])
api_v1_router.include_router(summarize_router, prefix='/summarize', tags=["Summarizing"])