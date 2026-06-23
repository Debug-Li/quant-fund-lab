from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class ApiResponse(BaseModel):
    success: bool
    message: str = ""
    data: Any | None = None
    error: str | None = None
    logs: list[str] = Field(default_factory=list)
