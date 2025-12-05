from idlelib.debugobj_r import remote_object_tree_item
import re
import bleach
from flask_wtf import FlaskForm
from markupsafe import Markup
from wtforms import StringField, PasswordField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp, ValidationError, regexp

# Username
RESERVED_USERNAMES = ['admin', 'root', 'superuser']

# Common Passwords
COMMON_PASSWORDS = ['123','2006','ILOVECATS','abcdef','footy']

ALLOWED_DOMAINS =  ['.edu','.ac.uk']


ALLOWED_TAGS = ['b', 'i', 'u', 'em', 'strong', 'a', 'p', 'ul', 'ol', 'li', 'br']
ALLOWED_ATTRIBUTES = ['href', 'title']

ALLOWED_PROTOCOL = ['https',]

class RegisterForm(FlaskForm):

    username = StringField('Username', validators=[
        DataRequired(message='Username must be between 3 and 20 characters long'),
        Email(message='Email address must be valid '),
        Length(min=3 , max=20, message='Username must be between 3 and 20 characters long')
    ])

    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=6, message='Password must be at least 6 characters long')
    ])

    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match')
    ])

    bio = TextAreaField('Bio', validators=[
        DataRequired(),
        Length(max = 1000, message='Bio must be at max 1000 characters')
    ])
    submit = SubmitField('Register')

    def validate_username(self, field):
        username = field.data.lower()

        if not any(username.endswith(domain) for domain in ALLOWED_DOMAINS):
            raise ValidationError('Username must end with one of the allowed domains')

        local_part = username.split("@")[0]
        if local_part in RESERVED_USERNAMES:
            raise ValidationError('Username must be between 3 and 20 characters long')

        BLACKLIST = [
            "Password123$", "Qwerty123!", "Adminadmin1@", "weLcome123!"
                ]



    def validate_password(self, field, BLACKLIST):

        pwd = field.data or ''
        username = self.username.data or ''

        if len(pwd) < 10:
            raise ValidationError("Password must be at least 10 characters long.")

        if not any(c.isupper() for c in pwd):
            raise ValidationError("Password must contain at least one uppercase letter.")

        if not any(c.isdigit() for c in pwd):
            raise ValidationError("Password must contain at least one digit.")

        if not re.search(r"[!@#$%^&*()\-_=+\[\]{}|;:'\",.<>?/`~]", pwd):
            raise ValidationError("Password must contain at least one special character.")


        if username and username.lower().split("@")[0] in pwd.lower():
            raise ValidationError("Password cannot contain your username.")

        if pwd in BLACKLIST:
            raise ValidationError("This password is not allowed.")


        if re.search(r"(.)\1\1", pwd):
            raise ValidationError("Password cannot contain repeated character sequences such as aaa, 111, !!!.")

    # Sanitization
    def sanitize_bio(self, bio_text: str) -> str:
        if not bio_text:
            return ''

        safe_html = bleach.clean(
            bio_text,
            tags=ALLOWED_TAGS,
            attributes=ALLOWED_ATTRIBUTES,
            protocols=ALLOWED_PROTOCOL,
            stip  = True
        )

        return Markup(safe_html)
