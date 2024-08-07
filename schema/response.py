from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class DocumentInfo(BaseModel):
    time: datetime
    text: str
class ClusterInfo(BaseModel):
    cluster_id: int
    documents: List[DocumentInfo]

class ClusterResponse(BaseModel):
    num_clusters: Optional[int] = None
    num_clustered_documents: Optional[int] = None
    num_noise_documents: Optional[int] = None
    clusters: Optional[List[ClusterInfo]] = None
    noise_documents: Optional[List[DocumentInfo]] = None

    @staticmethod
    def from_json(data: dict):
        return ClusterResponse(
            num_clusters=data["num_clusters"],
            num_clustered_documents=data["num_clustered_documents"],
            num_noise_documents=data["num_noise_documents"],
            clusters=[
                ClusterInfo(
                    cluster_id=cluster["cluster_id"], 
                    documents=[
                        DocumentInfo(
                            time=doc['time'], 
                            text=doc['text']
                        ) for doc in cluster["documents"]
                    ]
                ) for cluster in data["clusters"]
            ],
            noise_documents=[
                DocumentInfo(
                    time=doc['time'], 
                    text=doc['text']
                ) for doc in data["noise_documents"]["documents"]
            ]
        )
    
class SummarizeInfo(BaseModel):
    cluster_id: int
    time: datetime
    summarizeContent: str
    
class SummarizeResponse(BaseModel):
    summarizedCluster: Optional[List[SummarizeInfo]] = None
