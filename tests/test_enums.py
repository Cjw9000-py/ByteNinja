from byte_ninja.enums import StreamMode, ByteOrder


def test_stream_mode():
    flags = StreamMode.READ | StreamMode.WRITE | StreamMode.SEEK

    assert flags.can_read()
    assert flags.can_write()
    assert flags.can_seek()

    flags = StreamMode.READ

    assert flags.can_read()
    assert not flags.can_write()
    assert not flags.can_seek()

    flags = StreamMode.WRITE

    assert not flags.can_read()
    assert flags.can_write()
    assert not flags.can_seek()

    flags = StreamMode.SEEK

    assert not flags.can_read()
    assert not flags.can_write()
    assert flags.can_seek()


def test_byte_order():
    assert ByteOrder.LITTLE.as_literal() == 'little'
    assert ByteOrder.BIG.as_literal() == 'big'
