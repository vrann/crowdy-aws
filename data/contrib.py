"""
Contains contributor class and associated code.
"""
import uuid
import json


class Contributor:
    """
    Contains information about a specific contributor.
    """

    def __init__(self, **kwargs):
        self.id = kwargs.get('id', uuid.uuid4().int)
        self.name = kwargs.get('name', '')
        self.projects = kwargs.get('projects', {})
        for k, v in kwargs:
            if hasattr(self, k):
                setattr(self, k, v)
            else:
                raise ValueError('Unexpected kwd received: {}'.format(k))

    def add_pledged_hours(self, project_id: int, hours: float):
        """
        Adds a pledge of a number of hours to a project.
        :param project_id: int id of the project to which time has
                been pledged
        :param hours: float of number of hours pledged.
        :return: None
        """
        try:
            self.projects[project_id] += hours
        except KeyError:
            self.projects[project_id] = hours

    @property
    def as_json(self) -> str:
        return json.dumps({
            'id': self.id,
            'name': self.name,
            'projects': self.projects
        })

    @classmethod
    def from_json(cls, json_str: str) -> 'Contributor':
        return cls(**json.loads(json_str))
