import os
import pytest
from api_first import Pets

pt = Pets()


def test_register_and_delete_user():
    pets_register = Pets()
    status = pets_register.get_registered()
    assert status == 200


def test_get_token():
    token, status, user_id = pt.get_token()
    assert status == 200
    assert token is not None


def test_list_users():
    status, amount = pt.get_list_users()
    assert status == 200
    assert amount


def test_get_pet():
    pet_id, status = pt.get_pet()
    assert status == 200
    assert pet_id is not None


def test_get_pet_photo():
    status, link = pt.get_pet_photo()
    assert status == 200
    assert link is not None
