from newrelic.agent import (
    application_settings,
    function_wrapper,
    transient_function_wrapper,
)
from newrelic.common.encoding_utils import unpack_field
from newrelic.core.attribute_filter import AttributeFilter
from newrelic.core.config import apply_config_setting, flatten_settings
from newrelic.core.database_utils import SQLConnections


def override_application_settings(overrides):
    @function_wrapper
    def _override_application_settings(wrapped, instance, args, kwargs):
        try:
            original_settings = application_settings()
            backup = dict(original_settings)
            for name, value in overrides.items():
                apply_config_setting(original_settings, name, value)

            original_filter = original_settings.attribute_filter
            flat_settings = flatten_settings(original_settings)
            original_settings.attribute_filter = AttributeFilter(flat_settings)

            return wrapped(*args, **kwargs)
        finally:
            original_settings.__dict__.clear()
            for name, value in backup.items():
                apply_config_setting(original_settings, name, value)
            original_settings.attribute_filter = original_filter

    return _override_application_settings


def check_attributes(parameters, required_params={}, forgone_params={}):
    if required_params:
        for param in required_params["agent"]:
            assert param in parameters["agentAttributes"]

        for param in required_params["user"]:
            assert param in parameters["userAttributes"]

        for param in required_params["intrinsic"]:
            assert param in parameters["intrinsics"]

    if forgone_params:
        for param in forgone_params["agent"]:
            assert param not in parameters["agentAttributes"]

        for param in forgone_params["user"]:
            assert param not in parameters["userAttributes"]


def check_event_attributes(
    event_data, required_params, forgone_params, exact_attrs=None
):
    """Check the event attributes from a single (first) event in a
    SampledDataSet. If necessary, clear out previous errors from StatsEngine
    prior to saving error, so that the desired error is the only one present
    in the data set.
    """

    intrinsics, user_attributes, agent_attributes = next(iter(event_data))

    if required_params:
        for param in required_params["agent"]:
            assert param in agent_attributes
        for param in required_params["user"]:
            assert param in user_attributes
        for param in required_params["intrinsic"]:
            assert param in intrinsics

    if forgone_params:
        for param in forgone_params["agent"]:
            assert param not in agent_attributes
        for param in forgone_params["user"]:
            assert param not in user_attributes
        for param in forgone_params["intrinsic"]:
            assert param not in intrinsics

    if exact_attrs:
        for param, value in exact_attrs["agent"].items():
            assert agent_attributes[param] == value, ((param, value), agent_attributes)
        for param, value in exact_attrs["user"].items():
            assert user_attributes[param] == value, ((param, value), user_attributes)
        for param, value in exact_attrs["intrinsic"].items():
            assert intrinsics[param] == value, ((param, value), intrinsics)


def validate_transaction_event_attributes(
    required_params={}, forgone_params={}, exact_attrs={}, index=-1
):

    captured_events = []

    @transient_function_wrapper(
        "newrelic.core.stats_engine", "StatsEngine.record_transaction"
    )
    def _capture_transaction_events(wrapped, instance, args, kwargs):
        try:
            result = wrapped(*args, **kwargs)
        except Exception:
            raise
        else:
            event_data = instance.transaction_events
            captured_events.append(event_data)
            return result

    @function_wrapper
    def _validate_transaction_event_attributes(wrapped, instance, args, kwargs):
        _new_wrapper = _capture_transaction_events(wrapped)
        result = _new_wrapper(*args, **kwargs)

        assert captured_events, "No events captured"
        event_data = captured_events[index]
        captured_events[:] = []

        check_event_attributes(event_data, required_params, forgone_params, exact_attrs)

        return result

    return _validate_transaction_event_attributes


def validate_transaction_trace_attributes(
    required_params={}, forgone_params={}, should_exist=True, url=None, index=-1
):

    trace_data = []

    @transient_function_wrapper(
        "newrelic.core.stats_engine", "StatsEngine.record_transaction"
    )
    def _validate_transaction_trace_attributes(wrapped, instance, args, kwargs):

        result = wrapped(*args, **kwargs)

        # Now that transaction has been recorded, generate
        # a transaction trace

        connections = SQLConnections()
        _trace_data = instance.transaction_trace_data(connections)
        trace_data.append(_trace_data)

        return result

    @function_wrapper
    def wrapper(wrapped, instance, args, kwargs):
        _new_wrapper = _validate_transaction_trace_attributes(wrapped)
        result = _new_wrapper(*args, **kwargs)

        _trace_data = trace_data[index]
        trace_data[:] = []

        if url is not None:
            trace_url = _trace_data[0][3]
            assert url == trace_url

        pack_data = unpack_field(_trace_data[0][4])
        assert len(pack_data) == 2
        assert len(pack_data[0]) == 5
        parameters = pack_data[0][4]

        assert "intrinsics" in parameters
        assert "userAttributes" in parameters
        assert "agentAttributes" in parameters

        check_attributes(parameters, required_params, forgone_params)

        return result

    return wrapper
