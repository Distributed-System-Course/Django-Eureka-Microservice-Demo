from django.test import TestCase

# Create your tests here.

"""
{
    "projects": {
        "proj_1_id": {
            "max_group_num": 3
        }, 
        "proj_2_id": {
            "max_group_num": 3
        }, 
        "proj_3_id": {
            "max_group_num": 2
        }, 
        "proj_4_id": {
            "max_group_num": 4
        }
    },
    "wishes": [
        {
            "team_id": "team_id_1",
            "choices": [
                "proj_3_id", "proj_1_id", "proj_2_id"
            ]
        },
        {
            "team_id": "team_id_2",
            "choices": [
                "proj_1_id", "proj_3_id", "proj_2_id"
            ]
        },
        {
            "team_id": "team_id_3",
            "choices": [
                "proj_4_id", "proj_3_id", "proj_2_id"
            ]
        },
        {
            "team_id": "team_id_4",
            "choices": [
                "proj_3_id", "proj_1_id", "proj_2_id"
            ]
        }
    ]
}
"""
