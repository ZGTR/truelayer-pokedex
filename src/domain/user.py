from datetime import datetime
from munch import Munch

from src.bootstrap_stages.stage00.logger_setup import logger


class User(object):

    @classmethod
    def user_login(cls, username, password):
        user = UserModel.username_index.query_page(username).first()

        if not user:
            return False, "The Email you're trying to login with isn't registered with Neurofenix. Please make sure " \
                          "it's typed in correctly.", None, None, None

        user_password = user.password.strip().lower()
        if not user_password == password:
            return False, 'Incorrect Activation Code. Please try again.', None, None, None

        success, msg = UserModel.update_last_login(user)
        if not success:
            return False, msg, None, None, None

        # For flask_login
        # user_model = ModelUser.get_authenticated_user(user['id'])
        # login_user(user_model)

        access_token = create_access_token(identity=username)

        refresh_token = create_refresh_token(identity=username)

        return True, 'Successfully logged in', user, access_token, refresh_token

    @classmethod
    def user_signup(cls, data):
        try:
            username = data.username

            logger.error("step 01")
            user = UserModel.username_index.query_page(username).first()

            logger.error("step 02")
            if user:
                return False, user, 'An account with the same Email address already exists. ' \
                                    'Please make sure the Email you provided is correct or signup using a different email address.'

            logger.error("step 03")
            connection = Connection(region=DDbConstants.DB_REGION, host=DDbConstants.DB_HOST)
            with TransactWrite(connection=connection) as transaction:
                group = UsersGroups.get_group_by_type(data.user_group)

                # Create a user
                new_user = UserModel(
                    email=data.email,
                    username=data.username,
                    password=data.password,
                    firstname=data.firstname,
                    lastname=data.lastname,
                    country=data.country
                )
                transaction.save(new_user)

                # Add to group
                new_users_groups = UsersGroupsModel(user_id=new_user.id, user_groups_id=group.id)
                transaction.save(new_users_groups)

                # Add their membership
                new_membership = UsersMembershipsModel(user_id=new_user.id)
                transaction.save(new_membership)

                # Add leaderboard entry
                new_rankings = DayLeaderboardModel(
                    user_id=new_user.id,
                    firstname=new_user.firstname,
                    lastname=new_user.lastname,
                    rank=0,
                    reps=0,
                    secs=0,
                    mins=0,
                    updated=datetime.utcfromtimestamp(0)
                )
                transaction.save(new_rankings)


            return True, new_user.as_dict(), None
        except Exception as ex:
            logger.error(ex.args[0])
            return False, None, ex.args[0]

    @staticmethod
    def user_remove(data: Munch):
        user_id = data.user_id
        user = UserModel.get(hash_key=user_id)
        user.delete()
        return user
