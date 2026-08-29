"""
Created on 29 Aug 2026

@author: Bruno Beloff (bbeloff@me.com)

python -m unittest -v unit/security/test_token.py

https://realpython.com/python-testing/
https://www.jetbrains.com/help/pycharm/creating-tests.html
"""

import unittest
from collections import OrderedDict
from datetime import timedelta

import jwt

from mrcs_api.security.scope import Scope
from mrcs_core.data.json import JSONify
from mrcs_core.security.token import AccessToken, JWT, TokenData


# --------------------------------------------------------------------------------------------------------------------

class TestToken(unittest.TestCase):

    # TokenData tests ------------------------------------------------------------------------------------------------

    def test_token_data_construct(self):
        token_data = TokenData('user123', {Scope.OBSERVE})
        self.assertEqual('user123', token_data.sub)
        self.assertEqual({Scope.OBSERVE}, token_data.scopes)
        self.assertEqual(f"TokenData:{{sub:user123, scopes:{{{repr(Scope.OBSERVE)}}}}}", str(token_data))


    def test_token_data_as_json_without_expiry(self):
        token_data = TokenData('user123', {Scope.OBSERVE})
        jdict = token_data.as_json()

        self.assertIsInstance(jdict, OrderedDict)
        self.assertEqual('user123', jdict['sub'])
        self.assertEqual('OBSERVE', jdict['scope'])
        self.assertNotIn('exp', jdict)


    def test_token_data_as_json_with_expiry(self):
        token_data = TokenData('user123', {Scope.OBSERVE})
        jdict = token_data.as_json(expiry=1700000000)

        self.assertIsInstance(jdict, OrderedDict)
        self.assertEqual('user123', jdict['sub'])
        self.assertEqual('OBSERVE', jdict['scope'])
        self.assertEqual(1700000000, jdict['exp'])


    def test_token_data_jsonify(self):
        token_data = TokenData('user123', {Scope.OBSERVE})
        jstr = JSONify.dumps(token_data)
        self.assertEqual('{"sub": "user123", "scope": "OBSERVE"}', jstr)


    def test_token_data_decode(self):
        payload = {
            'sub': 'user123',
            'scope': 'OBSERVE ALTER_LAYOUT'
        }
        encoded = jwt.encode(payload, TokenData.SECRET_KEY, algorithm=TokenData.ALGORITHM)

        token_data = TokenData.decode(encoded)
        self.assertEqual('user123', token_data.sub)
        self.assertEqual({Scope.OBSERVE, Scope.ALTER_LAYOUT}, token_data.scopes)


    def test_token_data_decode_without_scopes(self):
        payload = {
            'sub': 'user123'
        }
        encoded = jwt.encode(payload, TokenData.SECRET_KEY, algorithm=TokenData.ALGORITHM)

        token_data = TokenData.decode(encoded)
        self.assertEqual('user123', token_data.sub)
        self.assertEqual(set(), token_data.scopes)


    def test_token_data_decode_missing_sub(self):
        payload = {
            'scope': 'OBSERVE'
        }
        encoded = jwt.encode(payload, TokenData.SECRET_KEY, algorithm=TokenData.ALGORITHM)

        with self.assertRaises(ValueError) as ctx:
            TokenData.decode(encoded)

        self.assertEqual('the username may not be None', str(ctx.exception))


    def test_token_data_decode_invalid_token(self):
        with self.assertRaises(jwt.PyJWTError):
            TokenData.decode('invalid.jwt.token')


    # AccessToken tests ----------------------------------------------------------------------------------------------

    def test_access_token_construct(self):
        token_data = TokenData('user123', {Scope.OBSERVE})
        delta = timedelta(hours=1)
        access_token = AccessToken(token_data, delta)

        self.assertEqual(token_data, access_token.data)
        self.assertEqual(delta, access_token.expires_delta)
        expected = (f"AccessToken:{{data:TokenData:{{sub:user123, scopes:{{{repr(Scope.OBSERVE)}}}}}, "
                    f"expires_delta:1:00:00}}")
        self.assertEqual(expected, str(access_token))


    def test_access_token_none_delta(self):
        access_token = AccessToken('token_string', None)

        self.assertEqual('token_string', access_token.data)
        self.assertIsNone(access_token.expires_delta)
        self.assertEqual('AccessToken:{data:token_string, expires_delta:None}', str(access_token))


    # JWT tests ------------------------------------------------------------------------------------------------------

    def test_jwt_construct(self):
        access = AccessToken('sample_token', None)
        token = JWT(access)

        self.assertEqual(access, token.access)
        self.assertEqual('bearer', token.token_type)
        self.assertEqual('JWT:{access:AccessToken:{data:sample_token, expires_delta:None}, token_type:bearer}',
                         str(token))


    def test_jwt_construct_custom_token_type(self):
        access = AccessToken('sample_token', None)
        token = JWT(access, token_type='custom')

        self.assertEqual(access, token.access)
        self.assertEqual('custom', token.token_type)
        self.assertEqual('JWT:{access:AccessToken:{data:sample_token, expires_delta:None}, token_type:custom}',
                         str(token))


    def test_jwt_as_header(self):
        access = AccessToken('sample_token', None)
        token = JWT(access)
        self.assertEqual({'Authorization': 'Bearer sample_token'}, token.as_header())

        custom_token = JWT(access, token_type='mac')
        self.assertEqual({'Authorization': 'Mac sample_token'}, custom_token.as_header())


    def test_jwt_construct_from_none_jdict(self):
        self.assertIsNone(JWT.construct_from_jdict(None))
        self.assertIsNone(JWT.construct_from_jdict({}))


    def test_jwt_construct_from_jdict(self):
        jdict = {
            'token_type': 'bearer',
            'access_token': 'test_token_string'
        }
        token = JWT.construct_from_jdict(jdict)

        self.assertIsNotNone(token)
        self.assertEqual('bearer', token.token_type)
        self.assertEqual('test_token_string', token.access.data)
        self.assertIsNone(token.access.expires_delta)


# --------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    unittest.main()
