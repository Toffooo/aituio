from roboparse import BaseRouter

from .base import LINKS


class ImportantDatesRouter(BaseRouter):
    def _fb_handle(self, data):
        _text = ""

        for item in data:
            content = item.text.strip()
            _text.format(content + " ")

        return _text

    def load(self):
        response = self.create_router_response(
            path=LINKS["important_dates"],
            linter={"type": "LIST", "tag": "td", "attrs": {"class": "t-text"}},
        )
        return response

    def get(self):
        response = self.create_router_response(
            path=LINKS["important_dates"],
            linter={
                "type": "ELEMENT",
                "tag": "div",
                "attrs": {"id": "rec308673276"},
                "children": {
                    "type": "ELEMENT",
                    "tag": "div",
                    "attrs": {"class": "t-container"},
                    "children": {
                        "type": "ELEMENT",
                        "tag": "div",
                        "attrs": {},
                    },
                },
            },
        )
        return response
