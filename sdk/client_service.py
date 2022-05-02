import json
import time

from decouple import config

plugin_id = config("EKP_PLUGIN_ID", default="developer-mode")


class ClientService:
    def __init__(self, sio):
        self.sio = sio

    def emit_busy(self, sid, collection_name):
        layer = {
            "id": f"busy-{collection_name}",
            "collectionName": "busy",
            "set": [{"id": collection_name, }],
            "timestamp": int(time.time())
        }
        self.emit_add_layers(sid, [layer])

    def emit_done(self, sid, collection_name):
        message = {
            "query": {
                "id": f'busy-{collection_name}',
            }
        }
        self.sio.emit('remove-layers', json.dumps(message), room=sid)

    def emit_menu(self, sid, icon, title, nav_link):
        """
        Sends menu layer from server to the client side
        """

        layer = {
            "id": f"{plugin_id}_menu_{nav_link}",
            "collectionName": "menus",
            "set": [
                {
                    "id": f"{plugin_id}_{nav_link}",
                    "icon": icon,
                    "title": title,
                    "navLink": nav_link,
                }
            ],
            "timestamp": int(time.time())
        }

        self.emit_add_layers(sid, [layer])

    def emit_page(self, sid, path, element):
        """
        Sends main page content from server to the client side
        """

        layer = {
            "id": f"{plugin_id}_page_{path}",
            "collectionName": "pages",
            "set": [
                {
                    "id": path,
                    "element": element
                }
            ],
            "timestamp": int(time.time())
        }

        self.emit_add_layers(sid, [layer])

    def emit_documents(self, sid, collection_name, documents):

        layer = {
            "id": f"{plugin_id}_{collection_name}",
            "collectionName": collection_name,
            "set": documents,
            "timestamp": int(time.time())
        }

        message = {
            "layers": [
                {
                    "id": collection_name,
                    "collectionName": collection_name,
                    "set": documents,
                    "timestamp": int(time.time())
                }
            ]
        }

        self.emit_add_layers(sid, [layer])

    def emit_add_layers(self, sid, layers):
        message = {
            "layers": layers
        }
        self.sio.emit('add-layers', json.dumps(message), room=sid)
