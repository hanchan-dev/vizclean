class CleaningLogger:
    def __init__(self):
        self.logs = {}

    def add(self, key, value):
        self.logs[key] = value

    def get_log(self):
        return self.logs


