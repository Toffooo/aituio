from roboparse import BaseRouter

from .base import LINKS


class AETStreamsRouter(BaseRouter):
    def load(self):
        response = self.create_router_response(
            path=LINKS["aet_streams"],
            linter={"type": "ELEMENT", "tag": "a", "attrs": {"rel": "noopener"}},
        )
        return response

    def get(self):
        response = self.create_router_response(
            path=LINKS["aet_streams"],
            linter={
                "type": "LIST",
                "tag": "div",
                "attrs": {"data-record-type": "859"},
                "children": {
                    "type": "ELEMENT",
                    "tag": "div",
                    "attrs": {"class": "t859"},
                },
            },
        )
        return response
