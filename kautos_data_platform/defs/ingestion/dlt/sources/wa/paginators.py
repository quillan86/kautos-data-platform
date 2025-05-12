from dlt.sources.helpers.rest_client.paginators import BasePaginator
from dlt.sources.rest_api.config_setup import register_paginator
from dlt.common.typing import DictStrAny, Optional, Sequence, Any
from requests import Response
from requests.models import PreparedRequest

class PostBodyOffsetPaginator(BasePaginator):
    """
    Custom paginator for World Anvil history API.
    """
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