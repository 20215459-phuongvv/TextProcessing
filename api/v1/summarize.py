import http
from schema.response import ClusterResponse
from config.env import ENV
from fastapi import APIRouter
from pydantic import BaseModel
from business.clustering.process import ClusterService

env = ENV()
router = APIRouter()

@router.get("/cluster-documents", response_model=ClusterResponse)
def cluster_content_type():
    return ClusterService.cluster_documents()