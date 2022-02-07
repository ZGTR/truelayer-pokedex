import math
import secrets
import sys
from collections import deque
from datetime import datetime
from typing import Union, Any

from pynamodb.exceptions import PynamoDBException
from pynamodb.models import Model
from pynamodb.pagination import ResultIterator

from src.domain import DayStreak
from src.helpers.math_helper import clamp, normalize_unclamped_max
from src.models import UserModel, DayLeaderboardModel, DayLeaderboardRankIndex
from src.bootstrap_stages.stage00.logger_setup import logger
from src.helpers import date_helper

MAX_VALUE = int(sys.float_info.max)


class PlayersRankings(object):
    def __init__(self):
        from src.domain.progress_tracking import ProgressTracking
        self.progress_tracking = ProgressTracking()

    def build_rankings_digest(self, current_user_id, limit=4):
        logger.error("Starting build_rankings_digest( " + str(current_user_id) + ", " + str(limit) + " )")

        today = date_helper.get_user_current_datetime(current_user_id)
        start_of_day = date_helper.start_of_day_offset(today, date_helper.get_users_utc_offset(current_user_id))
        descend = True
        rankings = []
        current_user_ldbd = DayLeaderboardModel.get(hash_key=current_user_id)
        try:
            descending = current_user_ldbd.day_leaderboard_rank_index.query(
                hash_key=DayLeaderboardModel.bank_default,
                scan_index_forward=False)
        except Exception as x:
            logger.exception("Couldn't access score index")
            descend = False

        logger.error("Creating output deque of length " + str(limit - 1))
        ranking_queue = deque(maxlen=limit - 1)
        countdown = -1
        index = 1
        zeroes_to_add = 0
        top: DayLeaderboardModel
        im_in = False

        current_user_ldbd.prepare_for_insertion(current_user_id, start_of_day)

        if descend:
            try:
                getting_top = True
                while getting_top:
                    top = descending.next()
                    if top.prepare_for_insertion(current_user_id, start_of_day):
                        getting_top = False
                        break
                index += 1
            except StopIteration:
                logger.exception("Stopped iterating at end of index")
                descend = False

        while descend:
            try:
                # exit condition
                # we have added enough users after our user, stop now
                if countdown == 0:
                    logger.error("Countdown exhausted, stopping descent")
                    descend = False
                    break

                # exit preparation loop
                # counts down the extra users to add after our user
                if countdown > 0:
                    countdown -= 1
                    logger.error("Countdown length is " + str(countdown))

                # iterate through the index
                descending_next = descending.next()
                # logger.error("Running ( " + str(index) + " )")

                fresh = descending_next.prepare_for_insertion(current_user_id, start_of_day)

                if fresh:
                    # insert current user if this user has the same score (first time only)
                    if not im_in and current_user_ldbd.rank == descending_next.rank:
                        logger.error("Operating on current user (" + str(index) + ")")
                        ranking_queue.append((index, current_user_ldbd))
                        im_in = True
                        # having inserted the current user, now finalise the leaderboard after (if available)
                        # - limit/2 more results, or
                        # - as many results as are missing from the leaderboard, whichever is greater
                        countdown = max(limit - len(ranking_queue) - 1, int(limit / 2))
                        logger.error("Countdown initial length is " + str(countdown))
                        index += 1

                    # insert this user, but avoid double-inserting the current user
                    if current_user_id != descending_next.user_id:
                        ranking_queue.append((index, descending_next))
                        index += 1
                else:
                    zeroes_to_add += 1

            except StopIteration:
                logger.exception("Stopped iterating at end of index")
                descend = False
                break

        # top result
        is_you = top.user_id == current_user_id
        logger.error("Adding top result to output" + " (our user)" if is_you else "")
        rankings.append(self.get_leaderboard_user_streaked_digest_dict(
            top,
            1,
            is_you=is_you
        ))

        # remaining leaderboard results
        for thing in ranking_queue:
            is_you = thing[1].user_id == current_user_id

            logger.exception("Adding result " + str(thing[0]) + " to output" + " (our user)" if is_you else "")

            rankings.append(
                self.get_leaderboard_user_streaked_digest_dict(
                    thing[1],
                    thing[0],
                    is_you=thing[1].user_id == current_user_id)
            )

        limit = clamp(limit, 0, len(rankings) + zeroes_to_add)

        # replace non-scoring non-me players with bots
        logger.error(
            "replace_zero_scoring_players_with_bots( " + str(current_user_id) + ", " + str(limit) + ", rankings )")
        rankings = self.replace_zero_scoring_players_with_bots(current_user_id, limit, rankings)
        rankings[0]["is_top_player"] = True

        logger.error("Ending build_rankings_digest( " + str(current_user_id) + ", " + str(limit) + " )")
        return {"rankings": rankings}

    def build_rankings_all(self, current_user_id):
        logger.error("Starting build_rankings_all( " + str(current_user_id) + " )")
        today = date_helper.get_user_current_datetime(current_user_id)
        start_of_day = date_helper.start_of_day_offset(today, date_helper.get_users_utc_offset(current_user_id))
        descend = True
        rankings = []
        zeroes = []
        current_user_ldbd = DayLeaderboardModel.get(hash_key=current_user_id)
        try:
            descending = current_user_ldbd.day_leaderboard_rank_index.query(
                hash_key=DayLeaderboardModel.bank_default,
                scan_index_forward=False)
        except PynamoDBException:
            descending = None
            logger.exception("Couldn't access score index")
            descend = False

        index = 1
        im_in = False
        zeroes_in = False
        reached_users_with_rank_zero = False

        current_user_ldbd.prepare_for_insertion(current_user_id, start_of_day)

        while descend:
            try:
                descending_next = descending.next()
                reached_users_with_rank_zero |= descending_next.rank == 0
                fresh = descending_next.prepare_for_insertion(current_user_id, start_of_day)

                if not fresh:
                    zeroes.append(descending_next)
                    logger.error("User " + str(descending_next.user_id) + " last exercised before today on " + str(
                        descending_next.updated))

                # insert current user if this user has the same score (first time only)
                if fresh and not im_in and descending_next.rank == current_user_ldbd.rank:
                    logger.error("Inserting user " + str(current_user_id)
                                 + " before " + str(descending_next.user_id) + " (" + str(index) + ")")
                    rankings.append(self.get_leaderboard_user_streaked_digest_dict(
                        current_user_ldbd,
                        index,
                        is_you=True
                    ))
                    index += 1
                    im_in = True
                    logger.error("Our user now added to list (" + str(index) + ")")

                # put in zero-entries for all users whose exercise is outdated
                if reached_users_with_rank_zero:
                    for zero in zeroes:
                        rankings.append(self.get_leaderboard_user_streaked_digest_dict(
                            zero,
                            index,
                            is_you=False
                        ))
                        index += 1
                    zeroes = []

                # insert this user, but avoid double-inserting the current user
                if fresh and descending_next.user_id != current_user_id:
                    logger.error("Appending user " + str(descending_next.user_id) + " (" + str(index) + ")")
                    rankings.append(self.get_leaderboard_user_streaked_digest_dict(
                        descending_next,
                        index,
                        is_you=False
                    ))
                    index += 1

            except StopIteration:
                logger.exception("Stopped iterating at end of index")
                descend = False

        rankings[0]["is_top_player"] = True

        logger.error("Ending build_rankings_all( " + str(current_user_id) + " )")
        return {"rankings": rankings}

    def replace_zero_scoring_players_with_bots(self, current_user_id, limit, rankings):
        rankings = self.remove_zero_score_players(current_user_id, rankings)
        self.increase_to_at_least_n_player_bots(rankings, limit)
        self.set_position_rankings_bots_only(rankings)
        return rankings

    def get_leaderboard_user_streaked_digest_dict(self, user, position, is_you=False, is_top_player=False):
        streak_days, is_streaked_today = DayStreak.get_user_day_streak_count(user.user_id)
        digest_dict = user.to_digest_dict(
            name_strategy=self.get_user_display_name_firstname_only,
            streak_days=streak_days,
            is_streaked_today=is_streaked_today,
            position=position,
            #            is_top_player=is_top_player,
            is_you=is_you)
        return digest_dict

    # TODO: Optimize this function and data structure with separate db tables with daily, weekly aggregations
    def get_today_ranking_response_for_user_legacy(self, current_user_id):
        chooser = self.progress_tracking.get_today_reps_and_minutes_and_streak
        strategy_display_name = self.get_user_display_name_firstname_only
        chooser_config = {}
        ranks = self.get_ranking_response_for_user(current_user_id, chooser, chooser_config, strategy_display_name, 4,
                                                   is_with_bots=True, is_remove_zero_score_players=True)

        return ranks

    def get_today_ranking_digest_for_user(self, current_user_id):
        try:
            return self.build_rankings_digest(current_user_id)
        except Exception:
            logger.exception("Failing over to legacy digest method")
            return self.get_today_ranking_response_for_user_legacy(current_user_id)

    def get_today_ranking_response_for_users_legacy(self, current_user_id):
        chooser = self.progress_tracking.get_today_reps_and_minutes_and_streak
        strategy_display_name = self.get_user_display_name_firstname_only
        chooser_config = {}
        ranks = self.get_ranking_response_for_users(current_user_id, chooser, chooser_config, strategy_display_name)
        return ranks

    def get_today_ranking_complete_for_user(self, current_user_id):
        try:
            return self.build_rankings_all(current_user_id)
        except Exception as x:
            logger.exception(x)
            return self.get_today_ranking_response_for_users_legacy(current_user_id)

    def get_week_ranking_response(self, current_user_id, selected_week_aggregator):
        from src.domain.progress_tracking_weekly import ProgressTrackingWeekly
        chooser = ProgressTrackingWeekly().get_week_stats_for_whole_week
        chooser_config = dict(
            selected_week_aggregator=selected_week_aggregator
        )
        strategy_display_name = self.get_user_display_name_firstname_only
        return self.get_ranking_response_for_user(current_user_id, chooser, chooser_config, strategy_display_name, 15,
                                                  is_with_bots=False, is_remove_zero_score_players=False)

    def build_unsorted_rankings(self, chooser, chooser_config, strategy_display_name):

        users = UserModel.get_users_allowed_response()
        rankings = list()

        for user in users:
            obj = self.calculate_scores(chooser, chooser_config, strategy_display_name, user)
            rankings.append(obj)

        return rankings

    def calculate_user_scores(self, chooser, chooser_config, user):
        user_reps_and_minutes_and_streak = chooser(user.id, **chooser_config)
        # TODO aw this feels like a big assumption about the chooser output
        # TODO aw is it really worth having a chooser like this if we need it to behave so specifically?
        reps = user_reps_and_minutes_and_streak['reps']['progress']['pie']
        minutes = user_reps_and_minutes_and_streak['minutes']['progress']['pie']
        sum_score = reps['progress_normalized'] + minutes['progress_normalized']
        sum_reps = reps['progress']
        sum_minutes = minutes['progress']

        return sum_score, sum_minutes, sum_reps, user_reps_and_minutes_and_streak

    def calculate_scores(self, chooser, chooser_config, strategy_display_name, user):
        sum_score, sum_minutes, sum_reps, user_reps_and_minutes_and_streak \
            = self.calculate_user_scores(chooser, chooser_config, user)
        logger.error("---- creating obj")
        obj = dict(
            user_id=user.id,
            username=strategy_display_name(user.firstname, user.lastname),
            sum_score=sum_score,
            sum_reps=sum_reps,
            sum_minutes=sum_minutes,
        )
        logger.error("---- adding streak if streak there be")
        if 'streak' in user_reps_and_minutes_and_streak:
            logger.error("---- yes there be")
            obj['streak'] = user_reps_and_minutes_and_streak['streak']
        logger.error("---- RETURNING")
        return obj

    def get_user_display_name_firstname_and_lastname(self, firstname, lastname):
        return "{0} {1}".format(firstname, lastname)

    def get_user_display_name_firstname_only(self, firstname, lastname):
        return firstname

    def get_user_display_name_firstname_initial_dot_lastname(self, firstname, lastname):
        return "{0}.{1}".format(firstname[0:1], lastname)

    def get_user_names_as_tuple(self, firstname, lastname):
        return firstname, lastname

    def get_ranking_response_for_users(self, current_user_id, chooser, chooser_config, strategy_display_name):
        rankings = self.build_unsorted_rankings(chooser, chooser_config, strategy_display_name)

        rankings.sort(key=lambda x: x['sum_score'], reverse=True)

        self.move_player_to_the_nearest_upper_rank(rankings, current_user_id)

        self.set_position_rankings(rankings)

        user_rank = self.get_rank(rankings, current_user_id)
        user_rank['is_you'] = True

        self.add_first_player(rankings, rankings)

        return dict(
            rankings=rankings
        )

    def get_ranking_response_for_user(self, current_user_id, chooser, chooser_config, strategy_display_name, n_players,
                                      is_with_bots, is_remove_zero_score_players):

        rankings = self.build_unsorted_rankings(chooser, chooser_config, strategy_display_name)

        n_players = clamp(n_players, 0, len(rankings))

        # Descending
        rankings.sort(key=lambda x: x['sum_score'], reverse=True)

        self.move_player_to_the_nearest_upper_rank(rankings, current_user_id)

        if is_remove_zero_score_players:
            rankings = self.remove_zero_score_players(current_user_id, rankings)

        if is_with_bots:
            self.increase_to_at_least_n_player_bots(rankings, n_players)

        self.set_position_rankings(rankings)

        # TODO: Optimize
        user_rank = self.get_rank(rankings, current_user_id)
        user_rank['is_you'] = True

        user_index = rankings.index(user_rank)
        index_start = clamp(user_index - math.ceil(n_players * (2 / 3)), 0, len(rankings) - 1)
        index_end = clamp(index_start + n_players, 0, len(rankings))
        surrounding_ranks = rankings[index_start: index_end]

        self.add_first_player(rankings, surrounding_ranks)

        return dict(
            rankings=surrounding_ranks
        )

    def move_player_to_the_nearest_upper_rank(self, rankings, user_id):
        user_rank = self.get_rank(rankings, user_id)
        user_index = self.get_rank_index(rankings, user_rank)

        nearest_rank = next(rank for rank in rankings if rank['sum_score'] == user_rank['sum_score'])
        nearest_rank_index = self.get_rank_index(rankings, nearest_rank)

        # Move the player closer, just one below the next rank
        if 0 <= nearest_rank_index < len(rankings):
            rankings.insert(nearest_rank_index, rankings.pop(user_index))

    def get_rank(self, rankings, user_id):
        return next((x for x in rankings if x['user_id'] == user_id), None)

    def get_rank_index_of_user_id(self, rankings, user_id):
        return rankings.index(self.get_rank(rankings, user_id))

    def get_rank_index(self, rankings, rank):
        return rankings.index(rank)

    def set_position_rankings(self, rankings):
        # start in the sensible place
        position = 1
        for ranking in rankings:
            ranking["position"] = position
            position += 1

    def set_position_rankings_bots_only(self, rankings):
        # start in the sensible place
        position = 1

        for ranking in rankings:
            if "is_bot" in ranking.keys() and ranking["is_bot"]:
                # give bots a ranking
                ranking["position"] = position
            else:
                # align ranking to current non-bot user
                position = max(ranking["position"], position)
                ranking["position"] = position

            # add one so the bots will be consistent with the result above
            position += 1

    def add_first_player(self, rankings, surrounding_ranks):
        if rankings[0] is not surrounding_ranks[0]:
            first = rankings[0]
            surrounding_ranks.insert(0, first)

        surrounding_ranks[0]['is_top_player'] = True

    def remove_zero_score_players(self, current_user_id, rankings):
        to_delete = list()

        for rank in rankings:
            if rank['sum_score'] == 0:
                if rank['user_id'] == current_user_id:
                    continue
                to_delete.append(rank)

        rankings = [x for x in rankings if x not in to_delete]

        return rankings

    def increase_to_at_least_n_player_bots(self, rankings, n=5):
        from src.domain import ProgressTracking

        names = ['Alannah', 'The.Phoenix', 'Neura.Feouna', 'Felix.The.Fenix', 'Neuroa']

        up_to_n = clamp(n - len(rankings), 0, len(names))

        if up_to_n < 1:
            return

        for x in range(up_to_n):
            sum_reps = secrets.randbelow(ProgressTracking.RECOMMENDED_PER_DAY_REPS)
            sum_minutes = secrets.randbelow(ProgressTracking.RECOMMENDED_PER_DAY_MINUTES)
            sum_reps_progress_normalized = normalize_unclamped_max(sum_reps, 0,
                                                                   ProgressTracking.RECOMMENDED_PER_DAY_REPS)
            sum_minutes_progress_normalized = normalize_unclamped_max(sum_minutes, 0,
                                                                      ProgressTracking.RECOMMENDED_PER_DAY_MINUTES)
            sum_score = sum_reps_progress_normalized + sum_minutes_progress_normalized
            name = secrets.choice(names)
            if name in names:  # to protect mocked tests
                names.remove(name)
            streak_days = secrets.randbelow(5)
            rankings.append(dict(
                is_bot=True,
                user_id="nfx_bot_" + str(x),
                username=name,
                sum_score=sum_score,
                sum_reps=sum_reps,
                sum_minutes=sum_minutes,
                streak=dict(
                    streak_days=streak_days,
                    is_streaked_today=streak_days > 0
                )
            ))

        rankings.sort(key=lambda x: x['sum_score'], reverse=True)

    def populate_leaderboard_table_from_sessions(self, force: bool = False):
        users = UserModel.get_users_allowed_response()
        ids = []

        for user in users:
            # if we don't want to force recreate the entire board:
            if not force:
                try:
                    current_user_ldbd = DayLeaderboardModel.get(hash_key=user.id)
                    # if this entry exists, skip creation
                    if current_user_ldbd is not None:
                        continue
                except PynamoDBException:
                    pass

            ids.append(user.id)

            obj = self.calculate_scores(
                self.progress_tracking.get_today_reps_and_minutes_and_streak,
                {},
                self.get_user_names_as_tuple,
                user
            )

            # get all that day's exercise sessions
            sessions = self.progress_tracking.get_today_game_sessions(user.id)
            updated = None

            # get the latest end date for those sessions
            if sessions is not None and len(sessions) > 0:
                for session in sessions:
                    if updated is None or session.end_date > updated:
                        updated = session.end_date

            if updated is None:
                updated = datetime.utcfromtimestamp(0)

            DayLeaderboardModel(user_id=user.id,
                                firstname=user.firstname,
                                lastname=user.lastname,
                                rank=obj["sum_score"],
                                reps=obj["sum_reps"],
                                secs=obj["sum_minutes"] * 60,
                                mins=obj["sum_minutes"],
                                updated=updated
                                ).save()

        return ids
