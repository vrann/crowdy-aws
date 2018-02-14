import elasticsearch as es
import os

from .project import Project
from .contrib import Contributor
import logging

ELASTIC_HOST = os.environ['ELASTIC_HOST']
ELASTIC_PORT = 80
PROJECTS_INDEX = 'projects'
PROJECTS_DOC_TYPE = 'project'
CONTRIB_INDEX = 'contributors'
CONTRIB_DOC_TYPE = 'contrib'


class Model:
    """
    Handles general data access and manipulation
    """
    def __init__(self):
        self.es = es.Elasticsearch([ELASTIC_HOST])

    # -----------------------------------------------------------------
    # PROJECT METHODS

    def store_project(self, project: Project):
        """
        Stores a passed project in db.
        :param project:  Project
        :return: None
        """
        self.es.create(
            index=PROJECTS_INDEX,
            doc_type=PROJECTS_DOC_TYPE,
            id=project.id,
            body=project.as_json
        )

    def get_project_json(self, project_id) -> str:
        """
        Gets a project as json from passed project id.
        :param project_id: uuid
        :return: str
        """
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        logger.info(PROJECTS_INDEX)
        logger.info(PROJECTS_DOC_TYPE)
        logger.info(ELASTIC_HOST)
        try:
            result = self.es.get(
                _source=True,
                index=PROJECTS_INDEX,
                doc_type=PROJECTS_DOC_TYPE,
                id=project_id
            )
        except ConnectionError as e:
            if hasattr(e, 'message'):
                print(e.message)
            else:
                print(e)

        return result

    def get_project(self, project_id):
        """
        Gets project from id
        :param project_id: int
        :return: Project
        """
        return Project.from_json(self.get_project_json(project_id))

    def del_project(self, project_id):
        """
        Deletes project identified by passed id.
        :param project_id: int
        :return:
        """
        self.es.delete(
            index=PROJECTS_INDEX,
            doc_type=PROJECTS_DOC_TYPE,
            id=project_id
        )

    # -----------------------------------------------------------------
    # CONTRIBUTOR METHODS

    def store_contributor(self, contrib: 'Contributor'):
        """
        Stores passed contributor in db.
        :param contrib: Contributor
        :return: None
        """
        self.es.create(
            index=CONTRIB_INDEX,
            doc_type=CONTRIB_DOC_TYPE,
            id=contrib.id,
            body=contrib.as_json
        )

    def get_contributor_json(self, contrib_id):
        """
        Returns json representation of contributor identified by
        passed id.
        :param contrib_id: int
        :return:
        """
        return self.es.get(
            index=CONTRIB_INDEX,
            doc_type=CONTRIB_DOC_TYPE,
            id=contrib_id
        )

    def get_contributor(self, contrib_id):
        """
        Gets Contributor from id.
        :param contrib_id: int
        :return: Contributor
        """
        return Contributor.from_json(self.get_contributor_json(contrib_id))

    def del_contributor(self, contrib_id):
        """
        Deletes contributor identified by passed contributor id.
        :param contrib_id: int
        :return:
        """

        self.es.delete(
            index=CONTRIB_INDEX,
            doc_type=CONTRIB_DOC_TYPE,
            id=contrib_id
        )

    def add_pledged_hours(self, contrib_id: int, project_id: int, hours):
        contributor = self.get_contributor(contrib_id)
        project = self.get_project(project_id)

        contributor.add_pledged_hours(project_id, hours)
        project.add_contributor_hours(contrib_id, hours)

        self.store_contributor(contributor)
        self.store_project(project)
