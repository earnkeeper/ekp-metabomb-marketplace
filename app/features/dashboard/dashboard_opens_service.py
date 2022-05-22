from db.box_opens_repo import BoxOpensRepo


class DashboardOpensService:
    def __init__(
        self,
        box_opens_repo: BoxOpensRepo
    ):
        self.box_opens_repo = box_opens_repo

    async def get_documents(self):
        opens = self.box_opens_repo.find_since_block_number(0, 10000)
        nodes = [
           {"node": 0, "name": "Rare",},
           { "node": 1, "name": "Epic",},
           { "node": 2, "name": "Legend",},
           { "node": 3, "name": "Mythic",},
           { "node": 4, "name": "Meta",},
           { "node": 5, "name": "Common Box",},
        ]
        
        links = [
                {"source": 5, "target": 0, "value": 2},
                {"source": 5, "target": 1, "value": 2},
                {"source": 5, "target": 2, "value": 2},
                {"source": 5, "target": 3, "value": 2},
                {"source": 5, "target": 4, "value": 2},
        ]
        doc = {
            "nodes": nodes,
            "links": links
            }
        return [doc]
