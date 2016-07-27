from enum import IntEnum


class UnitByte(IntEnum):

    byte = 2 ** 0
    kilobyte = 2 ** 10
    megabyte = 2 ** 20
    gigabyte = 2 ** 30
    terabyte = 2 ** 40
    petabyte = 2 ** 50
    exabyte = 2 ** 60
    zettabyte = 2 ** 70
    yottabyte = 2 ** 80

    @staticmethod
    def convert(byte_value, unitbyte):
        converted_value = None
        if unitbyte in UnitByte:
            converted_value = byte_value / unitbyte.value
        return converted_value

    @staticmethod
    def auto_convert(byte_value):
        used_unitbyte = UnitByte.yottabyte
        converted_value = byte_value / UnitByte.yottabyte
        for unitbyte in UnitByte:
            temp_value = byte_value / unitbyte.value
            if temp_value < 1024:
                used_unitbyte = unitbyte
                converted_value = temp_value
                break
        return converted_value, used_unitbyte

    @staticmethod
    def get_name_reduction(unitbyte):
        reductions_en = {
            UnitByte.byte: 'B',
            UnitByte.kilobyte: 'KB',
            UnitByte.megabyte: 'MB',
            UnitByte.gigabyte: 'GB',
            UnitByte.terabyte: 'TB',
            UnitByte.petabyte: 'PB',
            UnitByte.exabyte: 'EB',
            UnitByte.zettabyte: 'ZB',
            UnitByte.yottabyte: 'YB'
        }
        return reductions_en.get(unitbyte)


__all__ = ['UnitByte']
