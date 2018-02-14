"""
Contains Project class and associated code
"""

import json
import uuid


class Project:
    """
    A project with time
    """

    def __init__(self, project_id=None, **kwargs):
        self.id = project_id #or uuid.uuid4()
        self.title = ''
        self.description = ''
        self.technologies = set()
        self.due_date = None
        self.hours_goal = 0
        self.git_link = ''
        self.slack_link = ''
        self.contributors = {}
        self.created_date = None

        # initialize fields from passed kwargs
        for k, v in kwargs.items():
            if hasattr(self, k):
                setattr(self, k, v)
            else:
                raise ValueError('Unexpected kwd: {}'.format(k))

    def add_contributor_hours(self, contrib_id, hours):
        try:
            self.contributors[contrib_id] += hours
        except KeyError:
            self.contributors[contrib_id] = hours

    @property
    def as_json(self) -> str:
        return json.dumps({
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'technologies': self.technologies,
            'due_date': self.due_date,
            'hours_goal': self.hours_goal,
            'git_link': self.git_link,
            'slack_link': self.slack_link,
            'contributors': self.contributors,
            'created_date': self.created_date,
        })

    @classmethod
    def from_json(cls, json_s: str) -> 'Project':
        """
        Creates a project from passed json str.

        :param json_s: str
        :return: Project
        :raises ValueError if invalid data passed.
        """
        return cls(**json.loads(json_s))
