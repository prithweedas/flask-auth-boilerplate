from flaskrest import ma


class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'email')
