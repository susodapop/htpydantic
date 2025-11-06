# `htpydantic`: Pydantic Models that play nice with [`htpy`](https://github.com/pelme/htpy)

One reason why `htpy` is compelling for building web apps versus a tool like Jinja is that 
you can statically type check your code as you write it. Given that Pydantic does the same
at _runtime_, combining the two made a lot of sense to me.

This repository is here as a demonstration of a pattern. For my usage, inheriting from the
default `BaseModel` is more than sufficient. But if you already customize your models then
you should copy this code into your repository and swap out `BaseModel` hohwever you like.

## Usage

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
