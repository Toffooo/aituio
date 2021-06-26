from roboparse import BaseRouter
from roboparse.schemas import RouterResponse

from .base import LINKS


class JobsImageRouter(BaseRouter):
    def get(self) -> RouterResponse:
        response = self.create_router_response(
            path=LINKS["jobs_extract_img_link"],
            linter={
                "type": "ELEMENT",
                "tag": "div",
                "attrs": {"id": "rec309225814"},
                "children": {
                    "type": "ELEMENT",
                    "tag": "div",
                    "attrs": {"class": "t107"},
                    "children": {
                        "type": "ELEMENT",
                        "tag": "img",
                        "attrs": {"class": "t107__width"},
                    },
                },
            },
        )
        return response
