from extensions import db
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from app import app

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(20))
    email = db.Column(db.String(20))
    posts = db.relationship("Posts", backref="poster", lazy="dynamic")

    # RESET TOKEN FOR PASSWORD RESET
    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config["SECRET_KEY"], expires_sec)
        return s.dumps({"user_id" : self.id}).decode("utf-8")

    # VERIFY TOKEN FOR PASSWORD RESET
    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config["SECRET_KEY"])
        try:
            user_id = s.loads(token)["user_id"]
        except:
            return None

        return Users.query.get(user_id)

class Posts(db.Model):
    __bind_key__ = "Posts"
    id = db.Column(db.Integer, primary_key=True)
    post = db.Column(db.String(200))
    posted_at = db.Column(db.String(20))
    poster_id = db.Column(db.Integer, db.ForeignKey("users.id"))
