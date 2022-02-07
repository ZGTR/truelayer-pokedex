import datetime
from unittest import mock
from freezegun import freeze_time

import pytz
from src.domain.day_streak import DayStreak
from src.tests.base_test import BaseTest
from dateutil.tz import tzutc


class TestSDayStreak(BaseTest):

    @mock.patch("src.models.day_streak.DayStreakModel.streak_day.set")
    @mock.patch("src.models.day_streak.DayStreakModel.last_streak_day.set")
    @mock.patch("src.models.day_streak.DayStreakModel.get")
    @mock.patch("src.domain.day_streak.get_user_yesterday_datetime")
    @mock.patch("src.domain.day_streak.get_user_current_datetime")
    def test_on_play_today_update_streak(self, 
        getUserCurrentDatetimeMock,
        getUserYesterdayDatetime,
        dayStreakModelGetMock,
        dayStreakModelLSDSetMock, 
        dayStreakModelSDSetMock):

        # fake input
        fakeUserId = "1"
        timezoneInfo = pytz.timezone('America/New_York') # central standard time USA

        # config mocks
        getUserCurrentDatetimeMock.return_value = datetime.datetime(2022, 2, 2, 21, 53, 27, 206232, tzinfo=timezoneInfo)
        getUserYesterdayDatetime.return_value = datetime.datetime(2022, 2, 1, 21, 53, 27, 206232, tzinfo=timezoneInfo)
        streakMock = mock.MagicMock()
        streakMock.last_streak_day = datetime.datetime(2022, 2, 1, tzinfo=tzutc())
        streakMock.streak_day = 39
        fakeLastStreakDaySetAction = "fakeLastStreakDaySetAction"
        fakeStreakDaySetAction = "fakeStreakDaySetAction"

        dayStreakModelGetMock.return_value = streakMock
        dayStreakModelLSDSetMock.return_value = fakeLastStreakDaySetAction
        dayStreakModelSDSetMock.return_value = fakeStreakDaySetAction

        # testable function
        DayStreak.on_play_today_update_streak(fakeUserId)

        dayStreakModelLSDSetMock.assert_called_with(datetime.datetime(2022, 2, 2, 0, 0, tzinfo=tzutc()))
        dayStreakModelSDSetMock.assert_called_with(40)
        streakMock.update.assert_called_with([fakeLastStreakDaySetAction, fakeStreakDaySetAction])


    @mock.patch("src.models.day_streak.DayStreakModel.streak_day.set")
    @mock.patch("src.models.day_streak.DayStreakModel.last_streak_day.set")
    @mock.patch("src.models.day_streak.DayStreakModel.get")
    @freeze_time("2022-02-03T00:51:31.770000")
    def test_on_play_today_update_streak_fewer_mocks(self, 
        dayStreakModelGetMock,
        dayStreakModelLSDSetMock, 
        dayStreakModelSDSetMock):

        # fake input
        fakeUserId = "1"

        # config mocks
        streakMock = mock.MagicMock()
        streakMock.last_streak_day = datetime.datetime(2022, 2, 1, tzinfo=tzutc())
        streakMock.streak_day = 39
        fakeLastStreakDaySetAction = "fakeLastStreakDaySetAction"
        fakeStreakDaySetAction = "fakeStreakDaySetAction"

        dayStreakModelGetMock.return_value = streakMock
        dayStreakModelLSDSetMock.return_value = fakeLastStreakDaySetAction
        dayStreakModelSDSetMock.return_value = fakeStreakDaySetAction

        # testable function
        DayStreak.on_play_today_update_streak(fakeUserId)

        dayStreakModelLSDSetMock.assert_called_with(datetime.datetime(2022, 2, 3, 0, 0, tzinfo=tzutc()))
        dayStreakModelSDSetMock.assert_called_with(1)
        streakMock.update.assert_called_with([fakeLastStreakDaySetAction, fakeStreakDaySetAction])
