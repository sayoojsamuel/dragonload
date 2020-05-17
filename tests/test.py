#!/usr/bin/env python3

from dragonload.dragonload import startDragonload

def test_1_user():
    # Test dragonload for single user
    url = "http://www.ai.sri.com/movies/office.avi"
    user_count = 1
    user_id = 0
    user_list = [(0, "192.168.24.108")]
    startDragonload(url, user_count, user_id, user_list)

def test_2_user():
    url = "http://www.ai.sri.com/movies/office.avi"
    user_count = 2
    user_id = 0 # set 1 in other user
    user_list = [(0, "192.168.43.108"), (1, "192.168.43.194")]
    startDragonload(url, user_count, user_id, user_list)
