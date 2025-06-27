import requests

class FigmaClient:
    def __init__(self, access_token: str, file_key: str, node_key: str = None):
        self.access_token = access_token
        self.file_key = file_key
        self.node_key = node_key
        self.base_url = "https://api.figma.com/v1"

    def fetch_file(self):
        url = f"{self.base_url}/files/{self.file_key}"
        headers = {
            "X-Figma-Token": self.access_token
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    def fetch_node(self, node_key: str):
        url = f"{self.base_url}/files/{self.file_key}/nodes?ids={node_key}"
        headers = {
            "X-Figma-Token": self.access_token
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    def fetch_ui_elements(self):
        if not self.node_key:
            raise ValueError("node_key is required to fetch UI elements.")
        node_data = self.fetch_node(self.node_key)
        nodes = node_data.get("nodes", {})
        if self.node_key in nodes:
            document = nodes[self.node_key].get("document", {})
            return document.get("children", [])
        return []