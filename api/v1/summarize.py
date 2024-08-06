import http
from schema.response import SummarizeResponse
from config.env import ENV
from fastapi import APIRouter
from pydantic import BaseModel
from business.summarizing.summarize import SummarizeService

env = ENV()
router = APIRouter()

@router.get("/summarize-clusters", response_model=SummarizeResponse)
def cluster_content_type():
    return SummarizeService.summarize_documents()