import functools

from pymongo.errors import ConnectionFailure, OperationFailure
from pymongo.read_concern import ReadConcern
from pymongo.read_preferences import ReadPreference
from pymongo.write_concern import WriteConcern
from server.db.db_exception import ErrorDataDB


def run_transaction_with_retry(txn_func):
    @functools.wraps(txn_func)
    def wrapper(session, *args, **kwargs):
        while True:
            try:
                with session.start_transaction(
                    read_concern=ReadConcern(level="snapshot"),
                    write_concern=WriteConcern(w="majority"),
                    read_preference=ReadPreference.PRIMARY
                ):
                    return txn_func(session, *args, **kwargs)
            except (ConnectionFailure, OperationFailure) as ex:
                if ex.has_error_label("TransientTransactionError"):
                    print(
                        "INFO: TransientTransactionError,"
                        "Повторная попытка транзакции ..."
                    )
                    continue
                raise ErrorDataDB("Ошибка при попытке транзакции")
    return wrapper


def commit_with_retry(session):
    while True:
        try:
            session.commit_transaction()
            print("INFO: Transaction committed.")
            break
        except (ConnectionFailure, OperationFailure) as ex:
            if ex.has_error_label("UnknownTransactionCommitResult"):
                print(
                    "INFO: UnknownTransactionCommitResult,"
                    "Повторная попытка commit-операции ..."
                )
                continue
            raise ErrorDataDB("Ошибка при попытке транзакции")
