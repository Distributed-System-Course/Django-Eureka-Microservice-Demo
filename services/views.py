import json
from django.http.response import JsonResponse
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    return HttpResponse('Hello!')


""" Example Data:
{
    "projects": [
        {"id": "proj_1_id", "max_group_num": 1},
        {"id": "proj_2_id", "max_group_num": 1} 
    ],
    "wishes": [
        {
            "team_id": "team_id_1",
            "choices": [ "proj_1_id", "proj_2_id" ]
        },
        {
            "team_id": "team_id_2",
            "choices": [ "proj_1_id", "proj_2_id" ]
        }
    ]
}
"""

def grouping(request):
    data = dict()
    try:
        data = json.loads(request.body)
        # print('[Received]', data)
        max_group_num = {
            obj['id']: obj['max_group_num']
            for obj in data['projects']
        }
        wishes = data['wishes']
    except:
        return JsonResponse(dict())
    
    teams_of_proj = dict()

    for wish in wishes:
        for choice in wish['choices']:
            teams = teams_of_proj.get(choice, list())
            teams_of_proj[choice] = teams
            if len(teams) < max_group_num[choice]:
                teams.append(wish['team_id'])
                # first fit; if fit, then break
                break
    
    the_proj_of_team = dict()
    for project_id in teams_of_proj.keys():
        for team in teams_of_proj.get(project_id, list()):
            the_proj_of_team[team] = project_id
    
    return JsonResponse(the_proj_of_team)
