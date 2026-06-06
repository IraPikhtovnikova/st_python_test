from dataclasses import dataclass
from datetime import datetime

@dataclass
class Result:
    query: str
    sku: str
    position: int | str
    page: int | None
    total_checked: int
    timestamp: datetime

    def to_dict(self):
        return {
            "query": self.query,
            "sku": self.sku,
            "position": self.position,
            "page": self.page,
            "total_checked": self.total_checked,
            "timestamp": self.timestamp.isoformat(),
        }