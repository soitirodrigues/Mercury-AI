import sys

class BenchmarkError(Exception):
    pass

def check_regression():
    # ... existing code ...
    if threshold_exceeded:
        raise BenchmarkError(f"Threshold exceeded: {details}")

if __name__ == "__main__":
    try:
        check_regression()
        sys.exit(0)
    except BenchmarkError as e:
        print(f"[ERROR] {str(e)}")
        sys.exit(1)