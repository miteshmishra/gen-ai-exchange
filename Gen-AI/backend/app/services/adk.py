import os
from typing import List, Dict, Any

import vertexai
from vertexai.preview.generative_models import GenerativeModel, Part, Image
from google.oauth2 import service_account
from google.cloud import aiplatform

from app.core.config import settings

class ADKClient:
    def __init__(self, project_id: str = None, location: str = None, credentials = None):
        self.project_id = project_id or settings.GOOGLE_CLOUD_PROJECT
        self.location = location or settings.GOOGLE_CLOUD_LOCATION
        self.model_id = settings.ADK_MODEL_ID
        self.credentials = credentials or self._load_credentials()        
        if not self.project_id or not self.location or not self.credentials:
            raise ValueError("Google Cloud project ID, location, or credentials not configured.")

        vertexai.init(project=self.project_id, location=self.location, credentials=self.credentials)
        self.model = GenerativeModel(self.model_id)

    def _load_credentials(self):
        if settings.GOOGLE_APPLICATION_CREDENTIALS:
            return service_account.credentials.from_service_account_file(settings.GOOGLE_APPLICATION_CREDENTIALS)
        return None

    async def generate_content(self, prompt: str, images: List[str] = None) -> str:
        contents = [prompt]
        if images:
            for img_path in images:
                # In a real application, you'd load images from storage or convert base64
                # For this example, we'll assume img_path is a direct path to a local image
                # or a base64 encoded string that needs decoding.
                # For simplicity, let's assume it's a local path for now.
                try:
                    with open(img_path, "rb") as f:
                        img_bytes = f.read()
                    contents.append(Part.from_data(data=img_bytes, mime_type="image/jpeg"))
                except FileNotFoundError:
                    print(f"Warning: Image file not found at {img_path}")
                except Exception as e:
                    print(f"Error loading image {img_path}: {e}")

        response = await self.model.generate_content(contents)
        return response.text

def get_adk_client(project_id: str = None, location: str = None, credentials = None, mock_client: Any = None) -> ADKClient:
    if mock_client:
        return mock_client
    return ADKClient(project_id=project_id, location=location, credentials=credentials)