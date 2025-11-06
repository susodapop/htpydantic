from htpy import Element, div
from markupsafe import Markup
from pydantic import BaseModel

from htpydantic import HtPydanticModel


class C_Child(HtPydanticModel):
    name: str

    def to_htpy(self) -> Element:
        return div[self.name, self.children]


class C_Parent(HtPydanticModel):
    label: str = "Foo"

    def to_htpy(self) -> Element:
        return div[self.children]


def test_simple_render():
    """Demonstrate that components can mix-and-match with htpy"""
    output = div[C_Child(name="Zohran")]
    assert isinstance(output, Element)
    assert isinstance(str(output), Markup)
    assert str(output) == "<div><div>Zohran</div></div>"


def test_composability():
    """Demonstrate that htpydantic can include other components"""

    output = C_Parent(label="Bar")[
        C_Child(name="Zohran"), C_Child(name="Andrew"), C_Child(name="Curtis")
    ]
    assert isinstance(output, BaseModel)
    assert isinstance(output.to_htpy(), Element)
    assert isinstance(str(output), Markup)


def test_docstring_sample():
    class UserComponent(HtPydanticModel):
        user_id: int
        username: str

        def to_htpy(self) -> Element:
            return div(".user-info")[
                div[f"{self.username} ({self.user_id})"], div[self.children]
            ]

    el = div(".user-list")[
        UserComponent(user_id=1, username="Zohran")[
            "Some further information about Zohran"
        ],
        UserComponent(user_id=2, username="Andrew")[
            "Some further information about Andrew"
        ],
        UserComponent(user_id=3, username="Curtis")[
            "Some further information about Curtis"
        ],
    ]

    assert isinstance(el, Element)
    assert isinstance(str(el), Markup)
    assert str(el) == (
        """<div class="user-list">"""
        """<div class="user-info"><div>Zohran (1)</div><div>Some further information about Zohran</div></div>"""
        """<div class="user-info"><div>Andrew (2)</div><div>Some further information about Andrew</div></div>"""
        """<div class="user-info"><div>Curtis (3)</div><div>Some further information about Curtis</div></div>"""
        """</div>"""
    )
