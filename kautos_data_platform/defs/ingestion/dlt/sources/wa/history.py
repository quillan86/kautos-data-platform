"""
World Anvil API
Reference for REST API:
https://dlthub.com/docs/dlt-ecosystem/verified-sources/rest_api/basic

"""
import os
import dlt
from dlt.sources.rest_api import RESTAPIConfig, rest_api_resources
from dlt.sources.helpers.rest_client.paginators import BasePaginator
from dlt.sources.rest_api.config_setup import register_paginator
from dlt.common.typing import DictStrAny, Optional, Sequence, Any
from requests import Response
from requests.models import PreparedRequest


# Custom Paginator for POST body offset/limit
class PostBodyOffsetPaginator(BasePaginator):
    def __init__(
        self,
        limit: int,
        offset_param: str = "offset",
        limit_param: str = "limit",
        initial_offset: int = 0,
    ):
        super().__init__()
        self._limit = limit
        self._offset_param = offset_param
        self._limit_param = limit_param
        self._current_offset = initial_offset
        self._has_next_page = True

    @property
    def completed(self) -> bool:
        return not self._has_next_page

    def update_state(self, response: Response, data: Optional[Sequence[Any]]) -> None:
        if not data or len(data) < self._limit:
            self._has_next_page = False
        else:
            self._current_offset += self._limit

    def update_request_kwargs(self, request_kwargs: DictStrAny) -> None:
        request_json = request_kwargs.setdefault("json", {})
        # Ensure offset and limit are strings in the JSON body
        request_json[self._offset_param] = str(self._current_offset)
        request_json[self._limit_param] = str(self._limit)

    def update_request(self, request: PreparedRequest) -> PreparedRequest:
        return request

# Register the custom paginator
register_paginator("post_body_offset", PostBodyOffsetPaginator)


@dlt.source
def wa_history_source(source_name: str):
    # for consistency
    source_name = source_name.lower()
    # Get environment variables
    world_id = os.getenv(f"WORLDANVIL__{source_name.upper()}__WORLD_ID")
    api_key = os.getenv(f"WORLDANVIL__{source_name.upper()}__API_KEY") 
    app_key = os.getenv(f"WORLDANVIL__{source_name.upper()}__APP_KEY")

    # Add these print statements for debugging token values
    print(f"DEBUG: Using source_name for env var lookup: {source_name.upper()}")
    print(f"DEBUG: World ID retrieved: XXXXXX{world_id[-5:] if world_id and len(world_id) > 5 else world_id}X") # Mask most of it
    print(f"DEBUG: Auth Token retrieved: XXXXXX{api_key[-5:] if api_key and len(api_key) > 5 else api_key}X") # Mask most of it
    print(f"DEBUG: App Key retrieved: XXXXXX{app_key[-5:] if app_key and len(app_key) > 5 else app_key}X") # Mask most of it

    # Validate that environment variables are set
    if not all([world_id, api_key, app_key]):
        missing_vars = []
        if not world_id: missing_vars.append(f"WORLDANVIL__{source_name.upper()}__WORLD_ID")
        if not api_key: missing_vars.append(f"WORLDANVIL__{source_name.upper()}__API_KEY")
        if not app_key: missing_vars.append(f"WORLDANVIL__{source_name.upper()}__APP_KEY")
        raise ValueError(f"Missing environment variables: {', '.join(missing_vars)}")

    config: RESTAPIConfig = {
        "client": {
            "base_url": "https://www.worldanvil.com/api/external/boromir/",
            "headers": {
                "x-auth-token": app_key,
                "x-application-key": api_key,
                "Content-Type": "application/json",
                "accept": "application/json"
            },
        },
        "resource_defaults": {
            "primary_key": "id",
            "write_disposition": "merge",
        },
        "resources": [
            {
                "name": f"{source_name}_history_index",
                "endpoint": {
                    "path": "world/histories",
                    "method": "POST",
                    "params": {
                        "id": world_id
                    },
                    "paginator": {
                        "type": "post_body_offset",
                        "limit": 50,
                        "offset_param": "offset",
                        "limit_param": "limit"
                    }
                }
            },
            {
                "name": f"{source_name}_history_detail",
                "endpoint": {
                    "path": "history",
                    "params": {
                        "id": f"{{resources.{source_name}_history_index.id}}",
                        "granularity": 2
                    }
                },
                "include_from_parent": ["id"]
            }
        ]
    }



    yield from rest_api_resources(config)
