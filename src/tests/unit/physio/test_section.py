from src.domain.physio_progress_tracking_weekly import InformationBox
from src.tests.base_test import BaseTest


class TestSections(BaseTest):
    def test_roundAndTrimInSection_floatingPoint(self):
        section = InformationBox(
            title="Test",
            selected_count=1.111115,
            previous_count=0.01,
            unit='minute',
            percent=1.2345,
        )

        actual_dump = section.dump()
        expected_dump = dict(
            text_color='#28abe2',
            title='Test',
            subtitle='1.1 minutes more than previous period',
            count=1.1,
            unit='minutes',
            percent='1.2%',
            is_increased=True,
        )

        self.assertEqual(expected_dump, actual_dump)

    def test_roundAndTrimInSection_floatingPoint_noFloatingPointLeft(self):
        section = InformationBox(
            title="Test",
            selected_count=1.111115,
            previous_count=0.1,
            unit='minute',
            percent=1.2345,
        )

        actual_dump = section.dump()
        expected_dump = dict(
            text_color='#28abe2',
            title='Test',
            subtitle='1 minute more than previous period',
            count=1.1,
            unit='minutes',
            percent='1.2%',
            is_increased=True,
        )

        self.assertEqual(expected_dump, actual_dump)

    def test_roundAndTrimInSection_noFloatingPoint(self):
        section = InformationBox(
            title="Test",
            selected_count=34,
            previous_count=12,
            unit='minute',
            percent=145,
        )

        actual_dump = section.dump()
        expected_dump = dict(
            text_color='#28abe2',
            title='Test',
            subtitle='22 minutes more than previous period',
            count=34,
            unit='minutes',
            percent='145%',
            is_increased=True,
        )

        self.assertEqual(expected_dump, actual_dump)

    def test_roundAndTrimInSection_decrement(self):
        section = InformationBox(
            title="Test",
            selected_count=12,
            previous_count=34,
            unit='minute',
            percent=-21,
        )

        actual_dump = section.dump()
        expected_dump = dict(
            text_color='#28abe2',
            title='Test',
            subtitle='22 minutes less than previous period',
            count=12,
            unit='minutes',
            percent='21%',
            is_increased=False,
        )

        self.assertEqual(expected_dump, actual_dump)
