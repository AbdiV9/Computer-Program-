from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp, ValidationError, regexp

# Username
RESERVED_USERNAMES = ['admin', '', '', '', '', '', '', '']

# Common Passwords
COMMON_PASSWORDS = ['123','2006','ILOVECATS','abcdef','footy']

ALLOWED_DOMAINS =  ['.edu','.ac.uk']

class RegisterForm(FlaskForm):

    username = StringField('Username', validators=[
        DataRequired(),
        Email()
    ])

    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=6, message='Password must be at least 6 characters long')
    ])

    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match')
    ])

    bio = TextAreaField('Bio')
    submit = SubmitField('Register')

    def validate_username(self, field):
        if not any(field.data.endswith(domain) for domain in ALLOWED_DOMAINS):
            raise ValidationError('Invalid Username.')
        if field.data.lower() in RESERVED_USERNAMES:
            raise ValidationError('Username already taken. Please choose a different one.')


    def  validate_password(self, field):
        pwd = field.data or ''
        username = self.username.data or ''
        if pwd and len(pwd) < 6:
            raise ValidationError('Password must be at least 6 characters long')

        if any(char.isspace() for char in pwd):
            raise ValidationError("Password must not contain spaces.")
        if any(common.lower() == pwd.lower() for common in COMMON_PASSWORDS):
            raise ValidationError("Password is too common.")
        if username and username.lower() in pwd.lower():
            raise ValidationError("Password must not contain your username.")
        if not any(c.isupper() for c in pwd):
            raise ValidationError("Password must contain at least one uppercase letter.")
        if not any(c.islower() for c in pwd):
            raise ValidationError("Password must contain at least one lowercase letter.")
        if not any(c.isdigit() for c in pwd):
            raise ValidationError("Password must contain at least one number.")
        if not any(c in "!@#$%^&*()-_=+[]{}|;:'\",.<>?/`~" for c in pwd):
            raise ValidationError("Password must contain at least one special character.")