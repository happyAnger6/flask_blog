from flask_wtf import Form
from wtforms import (
    StringField,
    TextAreaField,
    PasswordField,
    BooleanField
)

from wtforms.validators import DataRequired, Length, EqualTo, URL

from webapp.models import User

class CommentForm(Form):
    name = StringField(
        'Name',
        validators=[DataRequired(), Length(max=255)]
    )
    text = TextAreaField(u'Comment', validators=[DataRequired()])

class LoginForm(Form):
    username = StringField('Username',[
        DataRequired(), Length(max=255)
    ])
    password = PasswordField('Password', [DataRequired()])

    def validate(self):
        check_validate = super(LoginForm, self).validate()

        if not check_validate:
            return False

        user = User.query.filter_by(
            username = self.username.data
        ).first()
        if not user:
            self.username.errors.append(
                'Invalid username or password'
            )
            return False

        if not self.user.check_password(self.password.data):
            self.username.errors.append(
                'Invalid username or password'
            )
            return False

        return True

class RegisterForm(Form):
    username = StringField('Username', [
        DataRequired(),
        Length(max=255)
    ]
    )
    password = PasswordField('Password', [
        DataRequired(),
        Length(min=8)
    ])
    confirm = PasswordField('Confirm Password', [
        DataRequired(),
        EqualTo('password')
    ])

    def validate(self):
        check_validate = super(RegisterForm, self).validate()

        if not check_validate:
            return False

        user = User.query.filter_by(
            username = self.username.data
        ).first()

        if user:
            self.username.errors.append(
                "User with that name already exists"
            )
            return False

        return True

class PostForm(Form):
    title = StringField('Title', [
        DataRequired(),
        Length(max=255)
    ])
    text = TextAreaField('Content', [DataRequired()])