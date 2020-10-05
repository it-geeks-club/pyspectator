from pyspectator.convert import UnitByte


def test_get_name_reduction():
    # Existing reduction
    reduction = UnitByte.get_name_reduction(UnitByte.megabyte)
    assert reduction == 'MB'
    # Non-existing reduction
    reduction = UnitByte.get_name_reduction('Non-existing reduction')
    assert reduction is None
