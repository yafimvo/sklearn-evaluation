import pytest
from unittest.mock import Mock, call
from ploomber_core.telemetry import telemetry
from sklearn_evaluation.telemetry import SKLearnEvaluationLogger

MOCK_API_KEY = 'phc_P1dsjk20bijsabdaib2eu'


@pytest.fixture
def mock_telemetry(monkeypatch):
    telemetry.Telemetry('ploomber', '0.14.0', MOCK_API_KEY)

    mock = Mock()
    mock_dt = Mock()
    mock_dt.now.side_effect = [1, 2]

    monkeypatch.setattr(telemetry.Telemetry, 'log_api', mock)
    monkeypatch.setattr(telemetry.datetime, 'datetime', mock_dt)
    monkeypatch.setattr(telemetry.sys, 'argv', ['/path/to/bin', 'arg'])

    yield mock


@pytest.mark.parametrize('action', ['some_action', None])
@pytest.mark.parametrize('feature', ['report', None])
@pytest.mark.parametrize('x', [1, None])
@pytest.mark.parametrize('y', [2, None])
@pytest.mark.parametrize('kwargs', [{'is_report': True, 'not-a-flag': True},
                                    {'not-a-flag': 'random-value'},
                                    {'is_report': True},
                                    {}])
def test_logger(mock_telemetry, action, feature, x, y, kwargs):
    flags = dict()
    function_arguments = dict(
        {
            'x': x,
            'y': y
        }
    )
    _action = action or 'my_function'

    @SKLearnEvaluationLogger.log(feature=feature, action=action)
    def my_function(a, b, x=None, y=None, **kwargs):
        pass

    my_function(1, 2, x=x, y=y, **kwargs)

    if len(kwargs) > 0:
        for key, value in kwargs.items():
            if key in SKLearnEvaluationLogger.flags():
                flags[key] = value

    expected_metadata = dict({
        'action': _action,
        'feature': feature,
        'args': function_arguments
    })

    if len(flags) > 0:
        expected_metadata['flags'] = flags

    mock_telemetry.assert_has_calls([
        call('sklearn-evaluation',
             metadata=expected_metadata)
    ])