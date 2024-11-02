def logDebug(msg: str) -> None:
    print("\033[2;30;43m", end="")
    print("DEBUG: " + msg, end="")
    print("\033[0;0m", end="\n")

def logSuccess(msg: str) -> None:
    print("\033[2;30;42m", end="")
    print("SUCCESS: " + msg, end="")
    print("\033[0;0m", end="\n")

def logFail(msg: str) -> None:
    print("\033[2;31;43m", end="")
    print("FAIL: " + msg, end="")
    print("\033[0;0m", end="\n")