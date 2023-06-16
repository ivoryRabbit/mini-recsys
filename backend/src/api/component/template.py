import logging
from functools import lru_cache
from typing import Optional

from fastapi.templating import Jinja2Templates

logger = logging.getLogger(__name__)

_template: Optional[Jinja2Templates] = None


def init_template():
    global _template
    _template = Jinja2Templates(directory="client/templates")


@lru_cache(maxsize=None)
def get_template() -> Jinja2Templates:
    global _template
    assert _template is not None
    return _template
