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
def wa_source(source_name: str):
    """
    World Anvil API source.
    """
    # for consistency
    source_name = source_name.lower()
    # Get environment variables
    world_id = os.getenv(f"WORLDANVIL__{source_name.upper()}__WORLD_ID")
    auth_token = os.getenv(f"WORLDANVIL__{source_name.upper()}__AUTH_TOKEN")
    app_key = os.getenv(f"WORLDANVIL__{source_name.upper()}__APP_KEY")

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
                    "response_actions": [
                        wrap_single_as_list
                    ]
                },
                "include_from_parent": ["id"],
            },
            {
                "name": "category_index",
                "endpoint": {
                    "path": "world/categories",
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
                "name": "category_detail",
                "endpoint": {
                    "path": "category",
                    "method": "GET",
                    "data_selector": "$",
                    "params": {
                        "id": "{resources.category_index.id}",
                        "granularity": 1
                    },
                    "paginator": "single_page",
                    "response_actions": [
                        wrap_single_as_list
                    ]
                },
                "include_from_parent": ["id"]
            },
            {
                "name": "article_index",
                "endpoint": {
                    "path": "world/articles",
                    "method": "POST",
                    "data_selector": "entities",                    
                    "params": {
                        "id": world_id
                    },
                    "json": {
                        # Only include articles for the category specified in the parent resource
                        "category": "{resources.category_index.id}"
                    },
                    "paginator": {
                        "type": "post_body_offset",
                        "limit": 50,
                        "offset_param": "offset",
                        "limit_param": "limit"
                    }
                },
                "include_from_parent": ["id"]
            },
            {
                "name": "article_detail",
                "endpoint": {
                    "path": "article",
                    "method": "GET",
                    "data_selector": "$",
                    "params": {
                        "id": "{resources.article_index.id}",
                        "granularity": 1
                    },
                    "paginator": "single_page",
                    "response_actions": [
                        wrap_single_as_list
                    ]
                }
            }
        ]
    }

    yield from rest_api_resources(config)
