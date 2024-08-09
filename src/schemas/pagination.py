from typing import List, TypeVar

from pydantic import BaseModel, Field

SchemaType = TypeVar("SchemaType", bound=BaseModel)


class Paginated[T](BaseModel):
    page: int
    per_page: int
    total: int
    results: List[T]


class PaginationParams(BaseModel):
    page: int = Field(1, ge=1)
    per_page: int = Field(10, ge=1, le=100)

    @property
    def skip(self) -> int:
        return (self.page - 1) * self.per_page

    @property
    def limit(self) -> int:
        return self.per_page
