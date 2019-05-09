#!/usr/bin/env python3

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

def serialize_user(user: dict, format: str):
    user = user["user"]
    if format == "human":
        return f'{user["id"]} {user["username"]}'
    elif format == "json":
        return json.dumps(user,indent=2)

def serialize_team(team: dict, format:str):
    if format == "human":
        return f'{team["id"]} {team["name"]} {len(team["members"])} users'
    elif format == "json":
        return json.dumps(team, indent=2)

def serialize_teams(teams: list, format: str):
    if format == "human":
        teams_str = [serialize_team(team, format) for team in teams]
        return "\n".join(teams_str)
    elif format == "json":
        return json.dumps(teams, indent=2)

def serialize_spaces(spaces: list, format: str):
    if format == "human":
        spaces_str = [f'{space["id"]} {space["name"]}' for space in spaces]
        return "\n".join(spaces_str)
    elif format == "json":
        return json.dumps(spaces, indent=2)

def serialize_projects(projects: list, format: str):
    if format == "human":
        projects_str = [f'{project["id"]} {project["name"]}' for project in projects]
        return "\n".join(projects_str)
    elif format == "json":
        return json.dumps(projects, indent=2)

def serialize_tasks(tasks: list, format: str):
    if format == "human":
        tasks_str = [f'{task["id"]} {task["name"]}' for task in tasks]
        return "\n".join(tasks_str)
    elif format == "json":
        return json.dumps(tasks, indent=2)

def serialize_default(obj, format):
    return json.dumps(obj, indent=2)

serializers = {
    "user": serialize_user,
    "teams": serialize_teams,
    "team": serialize_team,
    "spaces": serialize_spaces,
    "projects": serialize_projects,
    "tasks": serialize_tasks
}
def serialize(object_type: str, object: dict, format: str):
    if object_type not in serializers:
        raise SerializerDoesNotExist(object_type)
    return serializers[object_type](object, format)
