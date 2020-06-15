from datetime import datetime


class ErrorDataDB(Exception):
    """ Для исключений БД """
    def __init__(self, message):
        super(ErrorDataDB, self).__init__(message)
        self.message = message
        print("INFO: Exception ErrorDataDB.\n\t{}\n\t{}".format(
            datetime.utcnow().isoformat(),
            message
        ))

    def __str__(self):
        return str(self.message)
