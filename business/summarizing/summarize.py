import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from schema.response import SummarizeResponse, SummarizeInfo
from business.clustering.process import ClusterService
from datetime import datetime
from config.env import ENV

genai.configure(api_key=ENV.API_KEY)
model = genai.GenerativeModel(ENV.MODEL)
prompt = "Tóm tắt ngắn gọn các ý chính của đoạn thông tin sau trong một hoặc hai câu, giữ nguyên các từ viết tắt, tránh mất mát thông tin quan trọng:"
class SummarizeService:
    @staticmethod
    def summarize_documents() -> SummarizeResponse:
      data = ClusterService.cluster_documents()
      clusters_to_process = [cluster for cluster in data.clusters if len(cluster.documents) > 2]
      return SummarizeResponse(
        summarizedCluster=[SummarizeInfo(
            cluster_id=cluster.cluster_id, 
            time=datetime.now(), 
            summarizeContent=model.generate_content(
              prompt + ''.join(cluster.documents),
              safety_settings={
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_ONLY_HIGH,
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_ONLY_HIGH	
              }
            ).text
        ) for cluster in clusters_to_process]
      )
