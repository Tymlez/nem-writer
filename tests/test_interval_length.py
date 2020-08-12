from datetime import datetime, timedelta
import nemreader as nr
from nemwriter import NEM12


def test_15_minutes():
    """ should be able to write 15 minute files, and read them back correctly. """
    m = NEM12(to_participant="123")
    readings = [
        [datetime(2004, 4, 18, 0, 0) + timedelta(minutes=15 * (i + 1)), i, "A"]
        for i in range(24 * 4)
    ]
    m.add_readings(
        nmi="123",
        nmi_configuration="E1B1B2",
        nmi_suffix="E1",
        uom="kWh",
        interval_length=15,
        readings=readings,
    )
    output_filename = "tests/test_output_15_minute.csv"
    m.nem_output(file_path=output_filename)

    readback = nr.read_nem_file(output_filename)
    readback_readings = readback.readings["123"]["E1"]
    assert len(readback_readings) == len(readings)
    for i in range(len(readback_readings)):
        assert readback_readings[i].t_end == readback_readings[i].t_start + timedelta(
            minutes=15
        )
        assert readback_readings[i].t_end == readings[i][0]
        assert readback_readings[i].read_value == readings[i][1]
        assert readback_readings[i].quality_method == readings[i][2]
