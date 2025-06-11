import os

import pytest


@pytest.fixture(autouse=True, scope="session")
def initialize_agent():
    import newrelic_lambda.agent_protocol  # noqa
    import newrelic.agent

    settings = newrelic.agent.global_settings()
    settings.developer_mode = True
    settings.transaction_tracer.transaction_threshold = 0
    newrelic.agent.initialize()
    newrelic.agent.register_application(timeout=10.0)
    yield
    newrelic.agent.shutdown_agent()


@pytest.fixture(scope="session")
def readable_fifo():
    if os.path.exists("/tmp/newrelic-telemetry"):
        os.unlink("/tmp/newrelic-telemetry")
    os.mkfifo("/tmp/newrelic-telemetry")
    # This will block if we don't pass these flags
    fifo = os.open("/tmp/newrelic-telemetry", os.O_RDONLY | os.O_NONBLOCK)
    yield fifo
    os.close(fifo)
