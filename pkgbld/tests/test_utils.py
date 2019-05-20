"""
Tests of Package-Builder utility functions.
"""
# CODING-STYLE CHECKS:
# pycodestyle test_utils.py
# pylint --disable=locally-disabled test_utils.py

import pytest
from pkgbld.utils import os_call, channel_manager


def test_os_call():
    """
    Test call utility function.
    """
    assert os_call('hostname')
    with pytest.raises(OSError):
        os_call('illegal_os_command')


def test_channel_manager():
    # test that a channel is added and removed properly.
    assert "fake-channel" not in os_call("conda config --get channels").decode()
    with channel_manager(["fake-channel"]):
        assert "fake-channel" in os_call("conda config --get channels").decode()
    assert "fake-channel" not in os_call("conda config --get channels").decode()

    # test that channel_manager doesn't do anything when channels are not
    # specified.
    channel_info = os_call("conda config --get channels").decode()
    with channel_manager(None):
        assert channel_info == os_call("conda config --get channels").decode()

    # test that channel_manager ignores channels that are already used.
    with channel_manager(["already-exists"]):
        assert "already-exists" in os_call("conda config --get channels").decode()
        with channel_manager(["already-exists"]):
            pass
        # 'already-exists' should still be there after the context block is
        # closed.
        assert "already-exists" in os_call("conda config --get channels").decode()
