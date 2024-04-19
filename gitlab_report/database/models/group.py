from dataclasses import dataclass


@dataclass(kw_only=True, slots=True)
class Group:
    """GitLab group data."""

    id: int
    name: str

    def __hash__(self) -> int:
        return self.id

    def __str__(self) -> str:
        return self.name
