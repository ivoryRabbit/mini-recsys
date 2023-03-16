import math
import random
import logging
from collections import Counter
from typing import List, Tuple, Optional

from app.api.component.datamart import get_connection

logger = logging.getLogger(__name__)


class BestsellerService:
    def __init__(
        self,
        total_steps: int = 10000,
        alpha: float = 0.3,
        n_p: int = 100,
        n_v: int = 10,
        beta: float = 0.95,
    ):
        self.total_steps = total_steps
        self.alpha = alpha
        self.n_p = n_p
        self.n_v = n_v
        self.beta = beta
        self._connection = get_connection()

    def inference(self, queries: List[int], top_k: int = 10) -> List[int]:
        pass
