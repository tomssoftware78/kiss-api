import logging

from cicd.rest.response_chain.dummy_handler import DummyHandler
from cicd.rest.response_chain.environment_handler import EnvironmentHandler
from cicd.rest.response_chain.git_handler import GitHandler

class VersionResponseChainFactory():

    @property
    def logger(self):
        # Create a logger specific to this class
        if not hasattr(self, '_logger'):
            self._logger = logging.getLogger(self.__class__.__name__)
        return self._logger

    def create_version_response_chain(self):
        dummy_handler = DummyHandler()
        git_handler = GitHandler(dummy_handler)
        env_handler = EnvironmentHandler(git_handler)

        self.logger.debug("Creating a new VersionResponseChain - > EnvironmentHandler -> GitHandler -> DummyHandler")
        return env_handler