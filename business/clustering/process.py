from .data_fetcher import fetch_posts_from_mongodb
from .text_preprocessor import preprocess_documents
from .vectorizer import vectorize_documents
from .cluster import compute_distance_matrix, cluster_documents
from schema.response import ClusterResponse
from datetime import datetime
import json

class ClusterService:
    @staticmethod
    def cluster_documents() -> ClusterResponse:
        uri = "mongodb+srv://phuongvv:kjnhkjnh@vht.w3g8gh9.mongodb.net/?retryWrites=true&w=majority&appName=VHT"
        database_name = "vht"
        collection_name = "test"

        # Fetch data
        documents = fetch_posts_from_mongodb(uri, database_name, collection_name)

        # Preprocessing
        clean_documents = preprocess_documents(documents)

        # Remove empty documents after preprocessing
        clean_documents = [doc for doc in clean_documents if doc.strip()]

        # Check if there are any documents left after preprocessing
        if not clean_documents:
            print("All documents are empty after preprocessing.")
            return

        # Vectorize documents
        vectors = vectorize_documents(clean_documents)

        # Compute cosine distance matrix
        distance_matrix = compute_distance_matrix(vectors)

        # Clustering
        res_cluster = cluster_documents(distance_matrix)

        # Hiển thị kết quả
        # print("Number of clusters:", len(res_cluster))
        # print("Number of clustered documents:", len([j for i in res_cluster for j in i]))
        # print("Number of noise documents:", len(documents) - len([j for i in res_cluster for j in i]))
        # for i, cluster in enumerate(res_cluster):
        #     print("Cluster", i)
        #     for idx in cluster:
        #         print(documents[idx].split('\n')[0])
        #     print()

        # Tìm danh sách các tài liệu không thuộc cụm nào
        clustered_indices = {idx for cluster in res_cluster for idx in cluster}
        noise_documents = [documents[i].split('\n')[0] for i in range(len(documents)) if i not in clustered_indices]

        # Chuẩn bị dữ liệu để ghi vào tệp
        result_data = {
            "num_clusters": len(res_cluster),
            "num_clustered_documents": len(clustered_indices),
            "num_noise_documents": len(noise_documents),
            "clusters": [],
            "noise_documents": noise_documents
        }

        for i, cluster in enumerate(res_cluster):
            cluster_info = {
                "cluster_id": i,
                "documents": [documents[idx].split('\n')[0] for idx in cluster]
            }
            result_data["clusters"].append(cluster_info)

        # Ghi dữ liệu vào tệp JSON
        current_time = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        filename = f'clusters_{current_time}.json'
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(result_data, f, ensure_ascii=False, indent=4)

        # In ra để kiểm tra
        print("Number of clusters:", result_data["num_clusters"])
        print("Number of clustered documents:", result_data["num_clustered_documents"])
        print("Number of noise documents:", result_data["num_noise_documents"])
        # for cluster_info in result_data["clusters"]:
        #     print("Cluster", cluster_info["cluster_id"])
        #     for doc in cluster_info["documents"]:
        #         print(doc)
        #     print()
        return ClusterResponse.from_json(result_data)