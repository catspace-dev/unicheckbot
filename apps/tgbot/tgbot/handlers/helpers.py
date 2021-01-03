def check_int(value) -> bool:
    try:
        int(value)
    except ValueError:
        return False
    else:
        return True
