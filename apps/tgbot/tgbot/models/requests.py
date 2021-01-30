from tortoise import Model, fields


class UserCheckRequests(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField('models.User', related_name='requests')
    request = fields.CharField(max_length=255)
