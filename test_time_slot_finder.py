import unittest
import time_slot_finder
import datetime


class TestStringMethods(unittest.TestCase):
    def test_parse_date(self):
        (y, mo, d, h, mi) = time_slot_finder.parse_date("04/03/2018T12:00")
        self.assertEqual(y, 2018)
        self.assertEqual(mo, 4)
        self.assertEqual(d, 3)
        self.assertEqual(h, 12)
        self.assertEqual(mi, 0)

    def test_get_reserved_time_list(self):
        time_list = [{"start_time": "04/03/2018T12:00", "end_time": "04/03/2018T13:30"},
                     {"start_time": "04/03/2018T14:30", "end_time": "04/03/2018T15:30"}]
        expected = [(datetime.datetime(2018, 4, 3, 12, 0), datetime.datetime(2018, 4, 3, 13, 30)),
                    (datetime.datetime(2018, 4, 3, 14, 30), datetime.datetime(2018, 4, 3, 15, 30))]
        self.assertEqual(time_slot_finder.get_reserved_time_list(time_list), expected)

    def test_get_start_end_dates(self):
        time_list = [{"start_time": "04/03/2018T12:00", "end_time": "04/03/2018T13:30"},
                     {"start_time": "04/16/2018T14:30", "end_time": "04/16/2018T15:30"}]
        actual_start_date, actual_end_date = time_slot_finder.get_start_end_dates(time_list)
        expected_start_date = datetime.datetime(2018, 4, 3, 9, 0)
        expected_end_date = datetime.datetime(2018, 4, 16, 17, 0)
        self.assertEqual(actual_start_date, expected_start_date)
        self.assertEqual(actual_end_date, expected_end_date)

    def test_get_start_end_dates(self):
        time_list = [{"start_time": "04/03/2018T10:30", "end_time": "04/03/2018T17:00"},
                     {"start_time": "04/04/2018T10:00", "end_time": "04/04/2018T15:30"}]
        actual = time_slot_finder.find_time_slots(time_list)
        expected = [{'start_time': '04/03/2018T09:00', 'end_time': '04/03/2018T09:30'},
                    {'start_time': '04/03/2018T09:30', 'end_time': '04/03/2018T10:00'},
                    {'start_time': '04/03/2018T10:00', 'end_time': '04/03/2018T10:30'},
                    {'start_time': '04/04/2018T09:00', 'end_time': '04/04/2018T09:30'},
                    {'start_time': '04/04/2018T09:30', 'end_time': '04/04/2018T10:00'},
                    {'start_time': '04/04/2018T15:30', 'end_time': '04/04/2018T16:00'},
                    {'start_time': '04/04/2018T16:00', 'end_time': '04/04/2018T16:30'},
                    {'start_time': '04/04/2018T16:30', 'end_time': '04/04/2018T17:00'}]
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
