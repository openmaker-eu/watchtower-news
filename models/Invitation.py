import random
import string

from mongoengine import StringField, BooleanField, ReferenceField, CASCADE

from models.User import User
from models.Base import BaseDocument, BaseSchema

__author__ = 'Enis Simsar'


class Invitation(BaseDocument):
    user_id = ReferenceField(User, reverse_delete_rule=CASCADE)
    invitation_code = StringField(max_length=40, min_length=40, default=''.join(
        [random.choice(string.ascii_letters + string.digits) for _ in range(40)]))
    is_active = BooleanField(default=True)

    meta = {'collection': 'invitations'}

    def schema(self):
        return InvitationSchema()


class InvitationSchema(BaseSchema):
    class Meta:
        model = Invitation
