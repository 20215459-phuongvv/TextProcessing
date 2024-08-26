import time
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from schema.response import SummarizeResponse, SummarizeInfo, DocumentInfo
from business.clustering.process import ClusterService
from business.summarizing.data_fetcher import save_summarized_clusters
from datetime import datetime, timedelta
from config.env import ENV

genai.configure(api_key=ENV.API_KEY)
model = genai.GenerativeModel(ENV.MODEL)
uri = ENV.MONGO_URI
database_name = ENV.DATABASE_NAME
collection_name = ENV.COLLECTION_NAME
cluster_collection_name = ENV.CLUSTER_COLLECTION_NAME
safe_settings = {
  HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_ONLY_HIGH,
  HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
  HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
  HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_ONLY_HIGH	
}
prompt_1 = "Dựa vào các đoạn thông tin sau, cho tôi chủ đề chung nhất cho đoạn thông tin:"
prompt_2 = "Tóm tắt ngắn gọn các ý chính của đoạn thông tin sau trong một hoặc hai câu, giữ nguyên các từ viết tắt, tránh mất mát thông tin quan trọng:"

class SummarizeService:
    @staticmethod
    def generate_content_with_retry(prompt, max_retries=3):
        attempt = 0
        while attempt < max_retries:
            try:
                return model.generate_content(prompt, safety_settings=safe_settings).text
            except Exception as e:
                attempt += 1
                wait_time = 3 ** attempt  
                print(f"Resource exhausted. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
        raise Exception("Max retries exceeded for API request.")

    @staticmethod
    def summarize_documents() -> SummarizeResponse:
        data = ClusterService.cluster_documents()
        clusters_to_process = data.clusters

        now = datetime.now()
        start_of_day = datetime(now.year, now.month, now.day) - timedelta(days=8)
        end_of_day = start_of_day + timedelta(days=1) - timedelta(seconds=1)

        summarized_clusters = []
        
        for cluster in clusters_to_process:
            filtered_texts = ''.join(doc.text for doc in cluster.documents if start_of_day <= doc.time <= end_of_day)
            if filtered_texts:  # Ensure there's text to summarize
                title = SummarizeService.generate_content_with_retry(prompt_1 + filtered_texts)
                summary = SummarizeService.generate_content_with_retry(prompt_2 + filtered_texts)
                
                summarized_info = SummarizeInfo(
                    id = cluster.id,
                    cluster_id=cluster.cluster_id,
                    last_updated=start_of_day,
                    title=title,
                    summarized_events=[
                        DocumentInfo(
                            time=start_of_day,
                            text=summary
                        )
                    ],
                    documents=cluster.documents
                )
                summarized_clusters.append(summarized_info)
                time.sleep(1) 
                
        data = SummarizeResponse(summarized_cluster=summarized_clusters)
        
        save_summarized_clusters(uri, database_name, cluster_collection_name, data)
        return data
    
