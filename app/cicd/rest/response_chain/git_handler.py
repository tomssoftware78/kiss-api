import logging

from cicd.rest.response.version_response import VersionResponse
from cicd.rest.response_chain.abstract_handler import Handler

import git

class GitHandler(Handler):

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
        self.logger.debug("Looking for Version response data in git repository")


        # Get the latest tag (use the most recent tag if there are multiple)
        try:
            # Initialize git repository
            repo = git.Repo(search_parent_directories=True)

            git_tag = repo.git.describe('--tags', '--abbrev=0')
            print(git_tag)
            # Get the current commit hash
            git_commit = repo.head.object.hexsha

            if git_commit or git_tag:
                self.logger.debug("Version response data found (tag %s and commit %s)", git_tag, git_commit)
                return VersionResponse(tag=git_tag, commit=git_commit)

        except git.exc.GitCommandError as e:
            self.logger.error(f"Error: {e.stderr}")

        if self.next_handler:
          return self.next_handler.create_version_response()

        return VersionResponse(tag="git_tag", commit="git_commit")
