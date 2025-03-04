import requests

class OneMinAIAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.1min.ai/v1"

    def get_agents(self):
        """Retrieve list of available agents."""
        url = f"{self.base_url}/agents"
        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    def generate_text(self, agent_id, prompt):
        """Generate text using a specific agent."""
        url = f"{self.base_url}/generate"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "agent_id": agent_id,
            "prompt": prompt
        }
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()
