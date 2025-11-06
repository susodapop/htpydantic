import typing as t

from htpy import Element, div
from markupsafe import Markup
from pydantic import BaseModel, PrivateAttr


class HtPydanticModel(BaseModel):
    """
    A mixin to make your Pydantic models easily embeddable within htpy Elements.

    Just override to_htpy() to return any content that htpy can stringify and the
    rest just works.

    Any content slicded onto an instantiated HtPydanticMixin is available from its
    .children property.

    Usage:

    ```python
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
    ```

    This component will render as:

    ```html
    <div class="user-list">
        <div class="user-info">
            <div>Zohran (1)</div>
            <div>Some further information about Zohran</div>
        </div>
        <div class="user-info">
            <div>Andrew (2)</div>
            <div>Some further information about Andrew</div>
        </div>
        <div class="user-info">
            <div>Curtis (3)</div>
            <div>Some further information about Curtis</div>
        </div>
    </div>
    ```
    """

    _children: t.List[t.Any] = PrivateAttr(default_factory=list)

    def __getitem__(self, items: t.Any) -> t.Self:
        if not isinstance(items, (list, tuple)):
            items = [items]
        self._children = list(items)
        return self

    @property
    def children(self) -> t.List[t.Any]:
        """Returns the sequence of children that were sliced into this component.

        Allows you to accept arbitrary input that will be wrapped as a group
        """
        return self._children

    def to_htpy(self) -> Element:
        return div[f"to_htpy() not implemented in {type(self).__name__}"]

    def iter_chunks(self, context: t.Any) -> t.Iterable[str]:
        """This is the hook point that htpy uses to render this component
        when it is passed directly into a BaseElement
        """
        yield str(self.to_htpy())

    def __str__(self) -> Markup:
        """Mirrors htpy's behavior of BaseElement. Markup is a subclass of str which is
        a valid child of an htpy element. This returns str(self.to_htpy()) as a shorthand
        so that we can include components within the children of an htpy element without
        calling a special .render() method.
        """
        return Markup("".join(self.iter_chunks(context=None)))
