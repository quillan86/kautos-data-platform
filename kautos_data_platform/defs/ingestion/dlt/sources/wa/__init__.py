"""
World Anvil API
Reference for REST API:
https://dlthub.com/docs/dlt-ecosystem/verified-sources/rest_api/basic

"""
import os
import dlt
from dlt.sources.rest_api import RESTAPIConfig, rest_api_resources
from .paginators import PostBodyOffsetPaginator
from .helpers import wrap_single_as_list


@dlt.source
def wa_history_source(source_name: str):
    # logger.setLevel("DEBUG") # Re-commenting this for now to focus on response_actions
    # logger.info("DLT LOGGER level set to DEBUG.")

    # for consistency
    source_name = source_name.lower()
    # Get environment variables
    world_id = os.getenv(f"WORLDANVIL__{source_name.upper()}__WORLD_ID")
    auth_token = os.getenv(f"WORLDANVIL__{source_name.upper()}__AUTH_TOKEN")
    app_key = os.getenv(f"WORLDANVIL__{source_name.upper()}__APP_KEY")

    print(f"DEBUG (stdout): Using source_name for env var lookup: {source_name.upper()}")
    print(f"DEBUG (stdout): World ID retrieved: XXXXXX{world_id[-5:] if world_id and len(world_id) > 5 else world_id}X")
    print(f"DEBUG (stdout): Auth Token retrieved: XXXXXX{auth_token[-5:] if auth_token and len(auth_token) > 5 else auth_token}X")
    print(f"DEBUG (stdout): App Key retrieved: XXXXXX{app_key[-5:] if app_key and len(app_key) > 5 else app_key}X")

    # Validate that environment variables are set
    if not all([world_id, auth_token, app_key]):
        missing_vars = []
        if not world_id: missing_vars.append(f"WORLDANVIL__{source_name.upper()}__WORLD_ID")
        if not auth_token: missing_vars.append(f"WORLDANVIL__{source_name.upper()}__AUTH_TOKEN")
        if not app_key: missing_vars.append(f"WORLDANVIL__{source_name.upper()}__APP_KEY")
        raise ValueError(f"Missing environment variables: {', '.join(missing_vars)}")

    config: RESTAPIConfig = {
        "client": {
            "base_url": "https://www.worldanvil.com/api/external/boromir/",
            "headers": {
                "x-auth-token": auth_token,
                "x-application-key": app_key,
                "Content-Type": "application/json",
                "accept": "application/json"
            },
        },
        "resource_defaults": {
            "primary_key": "id",
            "write_disposition": "merge", # Or "replace" if preferred
        },
        "resources": [
            {
                "name": "history_index",
                "endpoint": {
                    "path": "world/histories",
                    "method": "POST",
                    "data_selector": "entities",                    
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
                "name": "history_detail",
                "endpoint": {
                    "path": "history",
                    "method": "GET",
                    "data_selector": "$",                    
                    "params": {
                        "id": "{resources.history_index.id}",
                        "granularity": 2
                    },
                    "paginator": "single_page",
                    "data_selector": "",
                    "response_actions": [
                        wrap_single_as_list
                    ]
                },
                "include_from_parent": ["id"],
            },
        ]
    }

    # logger.info(f"DLT LOGGER: wa_history_source configured for {source_name}. Ready to yield resources.")
    yield from rest_api_resources(config)
