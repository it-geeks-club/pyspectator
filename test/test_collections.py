import pytest
from pyspectator.collection import LimitedTimeTable
from datetime import timedelta, datetime
from time import sleep


def test_limited_time_table():
    time_span = timedelta(seconds=2)
    limited_time_table = LimitedTimeTable(time_span)
    assert len(limited_time_table) == 0
    with pytest.raises(TypeError):
        limited_time_table[int()] = 'record #1'
    first_record_dtime = datetime.now()
    limited_time_table[first_record_dtime] = 'record #1'
    assert first_record_dtime in limited_time_table
    sleep(0.1)
    limited_time_table[datetime.now()] = 'record #2'
    assert len(limited_time_table) == 2
    with pytest.raises(ValueError):
        future = datetime.now() + timedelta(days=1)
        limited_time_table[future] = 'record #2'
    sleep(2.1)
    limited_time_table[datetime.now()] = 'record #3'
    assert len(limited_time_table) == 2