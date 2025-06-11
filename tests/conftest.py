import newrelic.agent
import pytest


@pytest.fixture(autouse=True, scope="session")
def initialize_agent():
    settings = newrelic.agent.global_settings()
    settings.developer_mode = True
    settings.transaction_tracer.transaction_threshold = 0
    newrelic.agent.initialize()
    newrelic.agent.register_application(timeout=10.0)
    yield
    newrelic.agent.shutdown_agent()
