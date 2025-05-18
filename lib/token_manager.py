import json
from pathlib import Path

class TokenManager:
    def __init__(self):
        self.tokens_dir = Path("tokens")
        self.tokens_dir.mkdir(exist_ok=True)
        self.token_file = self.tokens_dir / "spotify_token.json"

    def save_token(self, token):
        """
        Save token to a file
        """
        with open(self.token_file, "w") as f:
            json.dump({"token": token}, f)

    def load_token(self):
        """
        Load token from file if it exists
        """
        if self.token_file.exists():
            with open(self.token_file, "r") as f:
                data = json.load(f)
                return data.get("token")
        return None

    def remove_token(self):
        """
        Remove token file if it exists
        """
        if self.token_file.exists():
            self.token_file.unlink() 