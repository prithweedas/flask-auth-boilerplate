from flaskrest.api.auth.schema import UserSchema

user_schema = UserSchema(strict=True)
users_schema = UserSchema(many=True, strict=True)
