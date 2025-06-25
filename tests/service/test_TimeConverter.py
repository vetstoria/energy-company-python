from src.service.time_converter import iso_format_to_unix_time, time_elapsed_in_hours

def test_iso_to_unix():
    assert iso_format_to_unix_time("1970-01-01T00:00:00") == 0
    assert iso_format_to_unix_time("1970-01-01T01:00:01") == 3601
    assert iso_format_to_unix_time("2020-02-29T23:12:41") == 1583017961

def test_elapsed_hours():
    earlier = iso_format_to_unix_time("2018-05-24T11:30:00")
    later = iso_format_to_unix_time("2018-05-24T12:00:00")
    assert time_elapsed_in_hours(earlier, later) == 0.5
