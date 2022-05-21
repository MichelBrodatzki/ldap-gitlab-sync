class Logger:
    verbosity = 0

    def __init__(self, verbosity):
        self.verbosity = verbosity

    def warning(self, message):
        if self.verbosity >= -1:
            print("[WARNING] {}".format(message))

    def log(self, message):
        if self.verbosity >= 0:
            print("[LOG] {}".format(message))

    def verbose(self, message):
        if self.verbosity >= 1:
            print("[INFO] {}".format(message))

    def debug(self, message):
        if self.verbosity >= 2:
            print("[DEBUG] {}".format(message))
