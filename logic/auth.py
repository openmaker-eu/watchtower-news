import hashlib
import logging
import random
import string
import uuid

from mongoengine import DoesNotExist, NotUniqueError

from models.Invitation import Invitation
from models.User import User

__author__ = 'Enis Simsar'


# from http://www.pythoncentral.io/hashing-strings-with-python/
def hash_password(password):
    # uuid is used to generate a random number
    salt = uuid.uuid4().hex
    return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt


# from http://www.pythoncentral.io/hashing-strings-with-python/
def check_password(hashed_password, user_password):
    password, salt = hashed_password.split(':')
    return password == hashlib.sha256(salt.encode() + user_password.encode()).hexdigest()


def register_user(invitation_code, username, password):
    password = hash_password(password)

    try:
        invitation = Invitation.objects.get(invitation_code=invitation_code, is_active=True)
    except DoesNotExist:
        return {'response': False, 'error': 'Invitation Code is invalid.'}
    except Exception as e:
        return {'response': False, 'error': e}

    try:
        user = User(username=username, password=password)
        user.save()
    except NotUniqueError:
        return {'response': False, 'error': 'Username is already registered!'}
    except Exception as e:
        return {'response': False, 'error': e}

    invitation.is_active = False
    invitation.save()

    return {'response': True, 'api_token': user.api_token}


def login_user(username, password):
    try:
        user = User.objects.get(username=username)
        if not check_password(user.password, str(password)):
            raise DoesNotExist
    except DoesNotExist:
        return {'response': False, 'error': 'Credentials are not correct!'}
    except Exception as e:
        return {'response': False, 'error': e}

    return {'response': True, 'api_token': user.api_token}


def get_user_profile(user_id):
    try:
        user = User.objects.get(id=user_id)
    except DoesNotExist:
        return {'response': False}
    except Exception as e:
        return {'response': False, 'error': e}

    if user:
        logging.info(user.to_dict())
        return user.to_dict()

    return {'response': False}


def refresh_api_token(user_id):
    try:
        user = User.objects.get(id=user_id)
    except DoesNotExist:
        return {'response': False}
    except Exception as e:
        return {'response': False, 'error': str(e)}

    if user:
        new_token = ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(40)])
        user.api_token = new_token
        user.save()
        return {'api_token': new_token, 'response': True}

    return {'response': False}


def get_user_with_api_token(api_token):
    try:
        user = User.objects.get(api_token=api_token)
    except DoesNotExist:
        return {'response': False}
    except Exception as e:
        return {'response': False, 'error': e}

    if user:
        return {
            'response': True,
            'id': user.id
        }

    return {'response': False}
