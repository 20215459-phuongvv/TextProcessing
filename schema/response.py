from pydantic import BaseModel
from typing import List, Optional

class ClusterInfo(BaseModel):
    cluster_id: int
    documents: List[str]

class ClusterResponse(BaseModel):
    num_clusters: Optional[int] = None
    num_clustered_documents: Optional[int] = None
    num_noise_documents: Optional[int] = None
    clusters: Optional[List[ClusterInfo]] = None
    noise_documents: Optional[List[str]] = None

    @staticmethod
    def from_json(data: dict):
        return ClusterResponse(
            num_clusters=data["num_clusters"],
            num_clustered_documents=data["num_clustered_documents"],
            num_noise_documents=data["num_noise_documents"],
            clusters=[ClusterInfo(cluster_id=cluster["cluster_id"], documents=cluster["documents"]) for cluster in data["clusters"]],
            noise_documents=data["noise_documents"]
        )
