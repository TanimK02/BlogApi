from marshmallow import Schema, fields


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str()
    email = fields.Str()
    password = fields.Str(required=True)
    name = fields.Str()


class PlainCommentSchema(Schema):
    id = fields.Int()
    content = fields.Str(required=True)
    published_at = fields.Str()
    updated_at = fields.Str()


class PostSchema(Schema):
    id = fields.Int()
    title = fields.Str(required=True)
    content = fields.Str(required=True)
    created_at = fields.Str(required=True)
    updated_at = fields.Str()
    published_at = fields.Str()
    status = fields.Str()
    summary = fields.Str()
    


class CommentSchema(PlainCommentSchema):
    post_id = fields.Int(required=True)
