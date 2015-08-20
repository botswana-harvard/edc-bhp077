
class BatchError(Exception):
    pass


class BatchSaveError(Exception):
    pass


class BatchReceiveError(Exception):
    pass


class BatchDuplicateItemError(Exception):
    pass


class AlreadyReceivedError(Exception):
    pass
