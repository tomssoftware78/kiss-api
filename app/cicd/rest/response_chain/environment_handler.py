import logging

from cicd.rest.response.version_response import VersionResponse
from cicd.rest.response_chain.abstract_handler import Handler

import os

class EnvironmentHandler(Handler):

    @property
    def logger(self):
        # Create a logger specific to this class
        if not hasattr(self, '_logger'):
            self._logger = logging.getLogger(self.__class__.__name__)
        return self._logger

    def __init__(self, next_handler=None):
        super().__init__(next_handler=next_handler)
        #create a logger specific to this class:

    def create_version_response(self):
        self.logger.debug("Looking for Version response data in environment variables")
        git_commit = os.getenv('GIT_COMMIT')
        git_tag = os.getenv('GIT_TAG')

        if git_commit or git_tag:
            self.logger.debug("Version response data found (tag %s and commit %s)", git_tag, git_commit)
            return VersionResponse(tag=git_tag, commit=git_commit)
        elif self.next_handler:
            self.logger.debug("Version response data not found in environment variables")
            return self.next_handler.create_version_response()
