#!/usr/bin/env python3

from collections import defaultdict
from functools import update_wrapper
import json

import requests

from .fuse import *

class Error(Exception):
    pass

class SerializerDoesNotExist(Error):
    pass

class Client:
    """An API client for click"""
    def __init__(self, api_key: str, url="https://api.clickup.com"):
        self.api_key = api_key
        self.url = url + "/api/v1/"
        self.session = requests.Session()
        self.session.headers.update({"Authorization": api_key})

    def _do(self, method, route, params=None, data=None):
        resp = self.session.request(
            method,
            self.url + route,
            params=params,
            data=data
        )
        resp.raise_for_status()
        return resp.json()

    def user(self):
        return self._do("GET", "user")

    def teams(self):
        return self._do("GET", "team")

    def team(self, id: str):
        return self._do("GET", f"team/{id}")

    def spaces(self, id: str):
        return self._do("GET", f"team/{id}/space")

    def projects(self, id: str):
        return self._do("GET", f"space/{id}/project")

    def create_list(self, project_id: str, list_name:str):
        data = {"name": list_name}
        return self._do("POST", f"project/{project_id}/list", data=data)

    def edit_list(self, project_id: str, list_name: str):
        data = {"name": list_name}
        return self._do("PUT", f"project/{project_id}/list", data=data)

    def tasks(self, team_id: str, **kwargs):
        """See documentation for all kwargs"""
        return self._do("GET", f"team/{team_id}/task", params=kwargs)

    def create_task(self, list_id:str, name:str, content:str, assignees:list, status:str, priority:int, due_date:str):
       data = {
           "name": name,
           "content": content,
           "assignees": assignees,
           "status": status,
           "priority": priority,
           "due_date": due_date
       }
       return self._do("POST", f"list/{list_id}/task")

    def edit_task(self, list_id:str, name:str, content:str, assignees:list, status:str, priority:int, due_date:str):
       data = {
           "name": name,
           "content": content,
           "assignees": assignees,
           "status": status,
           "priority": priority,
           "due_date": due_date
       }
       return self._do("PUT", f"list/{list_id}/task")

class SerializerFactory:
    def __init__(self):
        self.serializers = defaultdict(dict)

    def __call__(self, object_type: str, format: str):
        def wrapped(func):
            self.serializers[object_type][format] = func
            return func
        return wrapped

    def __contains__(self, key: tuple):
        object_type, format = key
        return object_type in self.serializers and format in self.serializers[object_type]

serializer = SerializerFactory()

@serializer("user", "human")
def user_human(user: dict):
    user = user["user"]
    return f'{user["id"]} {user["username"]}'

@serializer("team", "human")
def team_human(team: dict):
    return f'{team["id"]} {team["name"]} {len(team["members"])} users'

@serializer("teams", "human")
def teams_human(teams: list):
    teams_str = [team_human(team) for team in teams]
    return "\n".join(teams_str)

@serializer("spaces", "human")
def spaces_human(spaces: list):
    spaces_str = [f'{space["id"]} {space["name"]}' for space in spaces]
    return "\n".join(spaces_str)

@serializer("projects", "human")
def projects_human(projects: list):
    projects_str = [f'{project["id"]} {project["name"]}' for project in projects]
    return "\n".join(projects_str)

@serializer("tasks", "human")
def tasks_human(tasks: list):
    tasks_str = [f'{task["id"]} {task["name"]}' for task in tasks]
    return "\n".join(tasks_str)

def serialize(object_type: str, object: dict, format: str):
    if (object_type, format) not in serializer:
        raise SerializerDoesNotExist(object_type, format)
    elif object_type == "json":
        return json.dumps(object, indent=2)
    return serializer.serializers[object_type][format](object)
