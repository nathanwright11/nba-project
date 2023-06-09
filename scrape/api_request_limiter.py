import time


def api_req_lmtr(req_limit=13, wait=90):
    """Ensures all API requests comply with bbref restrictions."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            if wrapper.req_count >= req_limit:
                print(f"Request limit reached. {wait} second timeout")
                time.sleep(wait)
                wrapper.req_count = 0
            wrapper.req_count += 1
            return func(*args, **kwargs)
        wrapper.req_count = 0
        return wrapper
    return decorator