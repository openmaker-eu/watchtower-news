import logging

from mongoengine import DoesNotExist
import json

from models.Invitation import Invitation

__author__ = 'Enis Simsar'


def get_invitation(user_id, invitation_id):
    logging.info("user_id: {0}, invitation_id: {1}".format(user_id, invitation_id))
    if type(invitation_id) is not str:
        return {'error': 'invitation_id must be string!'}

    try:
        invitation = Invitation.objects.get(id=invitation_id, user_id=user_id)
    except DoesNotExist:
        return {}
    except Exception as e:
        logging.error("exception: {0}".format(str(e)))
        return {'error': str(e)}

    if invitation is None:
        return {}

    return invitation.to_dict()


def get_invitations(user_id):
    logging.info("user_id: {0}".format(user_id))
    try:
        invitations = Invitation.objects.filter(user_id=user_id)
    except DoesNotExist:
        return {}
    except Exception as e:
        logging.error("exception: {0}".format(str(e)))
        return {'error': str(e)}

    if invitations is None:
        return []

    invitations_json = []

    for invitation in invitations:
        invitations_json.append(invitation.to_dict())

    return json.dumps(invitations_json)


def post_invitation(user_id):
    logging.info("user_id: {0}".format(user_id))
    try:
        invitation = Invitation(user_id=user_id)
        invitation.save()
    except Exception as e:
        logging.error("exception: {0}".format(str(e)))
        return {'error': str(e)}

    return {
        'response': True,
        'invitation_id': invitation.to_dict()['id']
    }


def delete_invitation(user_id, invitation_id):
    logging.info("user_id: {0}, invitation_id: {1}".format(user_id, invitation_id))
    if type(invitation_id) is not str:
        return {'error': 'invitation_id must be string!'}

    try:
        invitation = Invitation.objects.get(id=invitation_id, user_id=user_id)
    except DoesNotExist:
        return {
            'message': 'invitation not found',
            'response': False
        }
    except Exception as e:
        logging.error("exception: {0}".format(str(e)))
        return {'error': str(e)}

    invitation.delete()

    return {'response': True}


def post_invitation_is_active(user_id, invitation_id, status):
    logging.info("user_id: {0}, invitation_id: {1}".format(user_id, invitation_id))
    if type(invitation_id) is not str:
        return {'error': 'invitation_id must be string!'}

    if type(status) is not int:
        return {'error': 'status must be integer!'}

    if status not in range(2):
        return {'error': 'status must be 0 or 1!'}

    try:
        invitation = Invitation.objects.get(id=invitation_id, user_id=user_id)
    except DoesNotExist:
        return {
            'message': 'invitation not found',
            'response': False
        }
    except Exception as e:
        logging.error("exception: {0}".format(str(e)))
        return {'error': str(e)}

    invitation.is_active = True if status == 1 else False

    invitation.save()

    return {'response': True}
