from django.test import TestCase
from django.urls import reverse

import json

# Create your tests here.

class TeamGroupingTests(TestCase):
    
    def get_result(self, data):
        response = self.client.post(reverse('services:grouping'), data=data, content_type='application/json')
        return json.loads(response.content)

    def test_empty_input(self):
        data = dict()
        self.assertEqual(len(self.get_result(data).keys()), 0)

    def test_regular_input_1(self):
        data = {
            "projects": [
                {"id": 1, "max_group_num": 5 }, # only allow one team
                {"id": 2, "max_group_num": 5 }  # only allow one team
            ],
            "wishes": [
                { # top priority
                    "team_id": "team_1",
                    "choices": [ 1, 2 ]
                },
                { # less priority
                    "team_id": "team_2",
                    "choices": [ 1, 2 ]
                }
            ]
        }
        self.assertDictEqual(
            self.get_result(data),
            { 'team_1': 1, 'team_2': 1 }
        )

    def test_competitive_input_1(self):
        data = {
            "projects": [
                {"id": 1, "max_group_num": 1}, # only allow one team
                {"id": 2, "max_group_num": 1}  # only allow one team
            ],
            "wishes": [
                { # top priority
                    "team_id": "team_1",
                    "choices": [ 1, 2 ]
                },
                { # less priority
                    "team_id": "team_2",
                    "choices": [ 1, 2 ]
                }
            ]
        }
        self.assertDictEqual(
            self.get_result(data),
            { 'team_1': 1, 'team_2': 2 }
        )

    def test_compititive_input_2(self):
        data = {
            "projects": [
                { "id": "1", "max_group_num": 0 }, 
                { "id": "2", "max_group_num": 1 }, 
                { "id": "3", "max_group_num": 1 }, 
                { "id": "4", "max_group_num": 1 }
            ],
            "wishes": [
                {
                    "team_id": "1",
                    "choices": [ "3", "1", "2" ]  # Got 3
                }, {
                    "team_id": "2",
                    "choices": [ "4", "3", "2" ]  # Got 4
                }, {
                    "team_id": "3",
                    "choices": [ "4", "3", "2" ]  # Miss 4, Miss 3, Got 2
                }, {
                    "team_id": "4",
                    "choices": [ "3", "1", "2" ]  # Miss 3, Miss 1, Miss 2, Got none (won't be mentioned in result)
                }
            ]
        }
        self.assertDictEqual(
            self.get_result(data),
            { '1': '3', '2': '4', '3': '2' }
        )

