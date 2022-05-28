from datetime import datetime

from db.activity_repo import ActivityRepo


class DashboardActivityService:
    def __init__(
        self,
        activity_repo: ActivityRepo,
    ):
        self.activity_repo = activity_repo

    def get_documents(self):
        
        models = self.activity_repo.find_all()
        
        now = datetime.now().timestamp()
        
        documents = []
        
        for model in models:
            
            model["updated"] = now
            
            document = {
                "day": model["day"],
                "id": model["id"],
                "new_users": model["new_users"],
                "timestamp_ms": model["timestamp"] * 1000,
                "updated": now,
            }
            documents.append(document)
        
        return documents