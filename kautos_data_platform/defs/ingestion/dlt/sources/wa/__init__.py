"""
World Anvil API
Reference for REST API:
https://dlthub.com/docs/dlt-ecosystem/verified-sources/rest_api/basic

"""

import dlt
from dlt.sources.rest_api import rest_api_source

source = rest_api_source({
    "client": {
        "base_url": "https://www.worldanvil.com/api/external/boromir/"

    },
    "resources": [

    ],
})