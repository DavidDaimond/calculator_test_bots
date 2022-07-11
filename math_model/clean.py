from datetime import datetime, timedelta
from collections.abc import Sequence

from base_objects import *


def count_clean(
        harvs: HarvesterPack,
        fields: Sequence[Field],
        is_two_tier: bool,
        start_date: datetime = None) -> timedelta:
    pass
