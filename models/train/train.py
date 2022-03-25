from dataclasses import dataclass
from typing import Hashable, Optional

from .train_status import TrainStatus


@dataclass
class Train:
    train_id: Hashable
    location: Hashable
    is_loaded: bool
    status: TrainStatus
    flow_destination: Optional[Hashable] = None

    def __str__(self) -> str:
        s = f'Train {self.train_id} ({"loaded" if self.is_loaded else "empty"}) at {self.location} '
        if self.status == TrainStatus.EN_ROUTE:
            if self.is_loaded:
                status_str = f'en route to {self.flow_destination}'
            else:
                status_str = f'en route from {self.flow_destination}'
        else:
            status_str = self.status.value.lower().replace('_', ' ')
        return s + status_str
