from db.box_opens_repo import BoxOpensRepo
from datetime import datetime

class DashboardOpensService:
    def __init__(
        self,
        box_opens_repo: BoxOpensRepo
    ):
        self.box_opens_repo = box_opens_repo


    def get_document(self, box_type, opens, now):
        root_index = 6

        nodes = {
            0: {"node": 0, "name": "Common", "value": 0},
            1: {"node": 1, "name": "Rare", "value": 0},
            2: {"node": 2, "name": "Epic", "value": 0},
            3: {"node": 3, "name": "Legend", "value": 0},
            4: {"node": 4, "name": "Mythic", "value": 0},
            5: {"node": 5, "name": "Meta", "value": 0},
            6: {"node": root_index, "name": f"{box_type}es Opened", "value": 0, "color": "yellow"},
        }

        links = {
            0: {"source": root_index, "target": 0, "value": 0},
            1: {"source": root_index, "target": 1, "value": 0},
            2: {"source": root_index, "target": 2, "value": 0},
            3: {"source": root_index, "target": 3, "value": 0},
            4: {"source": root_index, "target": 4, "value": 0},
            5: {"source": root_index, "target": 5, "value": 0},
        }

        for open in opens:
            if open["box_type"] != box_type:
                continue

            nodes[root_index]["value"] += 1
            nodes[open["hero_rarity"]]["value"] += 1
            links[open["hero_rarity"]]["value"] += 1

        for i in range(root_index):
            total = nodes[i]["value"]
            pc = round(
                nodes[i]["value"] * 100 / nodes[root_index]["value"], 2
            )
            nodes[i]["value"] = pc
            nodes[i]["name"] = f'{total} x {nodes[i]["name"]} ({pc}%)'

        total = nodes[root_index]["value"]
        nodes[root_index]["name"] = f'{total} x {nodes[root_index]["name"]}'

        doc = {
            "id": box_type,
            "updated": now,
            "nodes": list(nodes.values()),
            "links": list(links.values())
        }
        
        return doc        

    async def get_documents(self):
        opens = self.box_opens_repo.find_since_block_number(0, 10000)
        now = datetime.now().timestamp()
        return [
            self.get_document("Common Box", opens, now),
            self.get_document("Premium Box", opens, now),
            self.get_document("Ultra Box", opens, now),
        ]
