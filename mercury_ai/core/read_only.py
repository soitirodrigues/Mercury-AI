class ReadOnlyViolation(Exception):
    pass

def check_read_only(mode: bool):
    if mode:
        raise ReadOnlyViolation("Read Only Mode is enabled. Execution of orders is blocked.")
