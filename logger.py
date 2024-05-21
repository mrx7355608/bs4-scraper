class Logger:
    def __init__(self):
        self.logs = []

    def log(self, event) -> None:
        self.logs.append(event + "\n")
        return
    
    def clear_logs(self) -> None:
        self.logs = []
        return