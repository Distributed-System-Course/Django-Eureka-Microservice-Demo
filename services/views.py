import json
from django.http.response import JsonResponse
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    return HttpResponse('Hello!')


""" Example Data:
{
    "projects": {
        "proj_1_id": {"max_group_num": 3}, 
        "proj_2_id": { "max_group_num": 3}
    },
    "wishes": [
        {
            "team_id": "team_id_1",
            "choices": [
                 "proj_1_id", "proj_2_id"
            ]
        },
        {
            "team_id": "team_id_2",
            "choices": [
                "proj_1_id", "proj_2_id"
            ]
        }
    ]
}
"""

def grouping(request):
    data = json.loads(request.body)
    print(data)
    projects = data['projects']
    wishes = data['wishes']
    for wish in wishes:
        for choice in wish['choices']:
            choice = str(choice)
            teams = projects[choice].get('teams', list())
            if len(teams) < projects[choice]['max_group_num']:
                teams.append(wish['team_id'])
                projects[choice]['teams'] = teams
                break
    
    teams = dict()
    for project_id in projects.keys():
        for team in projects[project_id].get('teams', list()):
            teams[team] = project_id
    
    return JsonResponse(teams)
