import json
from requests import Response

def wrap_single_as_list(resp: Response, *a, **k):
    """
    Custom response hook for World Anvil history API.
    This is used to handle the case where the API returns a single object
    instead of a list of objects.
    """
    if resp.headers.get("content-type", "").startswith("application/json"):
        # turn {"id": ...}  →  [{"id": ...}]
        obj = resp.json()
        resp._content = json.dumps([obj]).encode()
    return resp
