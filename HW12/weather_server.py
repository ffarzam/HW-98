import requests as rq


class ConnectionManager:
    def __init__(self, final_url: str):
        self.final_url = final_url

    def __enter__(self):
        self.file = rq.get(self.final_url)
        return self.file

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.file.close()