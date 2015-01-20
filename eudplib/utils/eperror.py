class EPError(Exception):
    pass


def ep_assert(statement, message="Assertion failed"):
    if not statement:
        raise ut.EPError(message)
