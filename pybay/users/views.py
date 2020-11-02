import re
from aiohttp import web

from core import decorators, errors, security
from users import controllers


class Register(web.View):
    async def validate(self, data):
        errors_fields = {}

        email = data.get('email')
        if email:
            if re.match(r'[^@]+@[^@]+\.[^@]+', email):
                if await controllers.Users.get_by_email(email):
                    errors_fields['email'] = 'User with the same email already exists'
            else:
                errors_fields['email'] = 'Email is invalid'
        else:
            errors_fields['email'] = 'Email is required'

        password = data['password']
        if password:
            if len(password) < 8:
                errors_fields['password'] = 'Password must has 8 or more letters'
        else:
            errors_fields['password'] = "Password is required"

        username = data['username']
        if username:
            if len(username) >= 3:
                if await controllers.Users.get_by_username(username):
                    errors_fields['username'] = 'User with the same name already exists'
            else:
                errors_fields['username'] = 'Username must has 3 or more letters'
        else:
            errors_fields['username'] = 'Username is required'

        if errors_fields:
            raise errors.HTTP400Fields(errors_fields)

    @decorators.json_body
    async def post(self):
        data = self.request['data']
        await self.validate(data)
        u = await controllers.Users.register(data["email"], data["password"], data["username"])
        token = security.generate_jwt(u.id)

        return web.json_response({
            'id': str(u.id),
            'email': u.email,
            'username': u.username,
            'token': token,
        })


class Login(web.View):
    @decorators.json_body
    async def post(self):
        data = self.request['data']
        email = data.get('email')
        password = data.get('password')
        if not (email and password):
            raise errors.HTTP403('Email or password is incorrect')

        u = await controllers.Users.get_by_email(email)
        if not ( u and security.check_password_hash(password, u.hash_password)):
            raise errors.HTTP403('Email or password is incorrect')
        token = security.generate_jwt(u.id)

        return web.json_response({
            'token': token,
        })
