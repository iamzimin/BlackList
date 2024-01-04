class Log:
    @staticmethod
    def save_log(message):
        try:
            with open("log.txt", "a") as log_file:
                log_file.write(message + "\n")
        except Exception:
            pass
