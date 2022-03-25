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
