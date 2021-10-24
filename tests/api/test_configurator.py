import pytest
import os
import json
from django.urls import reverse
from django.core.management import call_command, base
from rest_framework.test import APIClient


@pytest.fixture
def valid_base_conf():
    base_conf = {
        "strategy_index": 1,

        "details": {
            "threshold": 0.5,
            "buffer_size": 6
        },

        "model": {
            "type": "A",
            "unit": 5,
            "max_age": 5,
            "calculation_cost": 0.3
        }
    }
    return base_conf


@pytest.fixture
def valid_params_conf():
    params_conf = {
        "strategy_index": [1,2,3,4,5],

        "details": {
            "threshold": [0.1, 0.2]
        },

        "model": {
            "max_age": [5,10,15,20],
            "type": ["A","B","C"]
        }
    }
    return params_conf


@pytest.fixture
def invalid_params_conf():
    params_conf = {
        "strategy_index": [1,2,3,4,5],

        "details": {
            "invalid_param": [0.1, 0.2]
        },

        "model": {
            "max_age": [5,10,15,20],
            "type": ["A","B","C"]
        }
    }
    return params_conf


def test_create_conf_using_command(tmpdir, valid_base_conf, valid_params_conf):
    test_directory = tmpdir.mkdir("test")
    test_directory.join("base_file.json").write(json.dumps(valid_base_conf))
    test_directory.join("params_file.json").write(json.dumps(valid_params_conf))

    args = [os.path.join(test_directory, "base_file.json"), os.path.join(test_directory, "params_file.json")]

    result = call_command("create_configurator", *args)

    assert result == "Successfully generated configurations"


def test_create_conf_using_command_with_invalid_param(tmpdir, valid_base_conf, invalid_params_conf):
    test_directory = tmpdir.mkdir("test")
    test_directory.join("base_file.json").write(json.dumps(valid_base_conf))
    test_directory.join("params_file.json").write(json.dumps(invalid_params_conf))

    args = [os.path.join(test_directory, "base_file.json"), os.path.join(test_directory, "params_file.json")]

    result = call_command("create_configurator", *args)

    assert result == "Wrong params config file. These params do not exist in base file: ['invalid_param']"


def test_create_conf_using_command_with_invalid_file(tmpdir, valid_base_conf, valid_params_conf):
    test_directory = tmpdir.mkdir("test")
    test_directory.join("base_file.png").write(valid_base_conf)
    test_directory.join("params_file.png").write(valid_params_conf)

    args = [os.path.join(test_directory, "base_file.png"), os.path.join(test_directory, "params_file.png")]
    try:
        call_command("create_configurator", *args)
    except Exception:
        assert True


def test_create_conf_using_command_with_invalid_args():
    try:
        call_command("create_configurator")
    except base.CommandError:
        assert True


def test_create_conf_using_API(valid_base_conf, valid_params_conf):
    client = APIClient()
    data = {
        "base": valid_base_conf,
        "params": valid_params_conf
    }

    response = client.post("/v1/configurator/", data=data, format="json")
    assert response.status_code == 200


def test_create_conf_using_API_with_invalid_params(valid_base_conf, invalid_params_conf):
    client = APIClient()
    data = {
        "base": valid_base_conf,
        "params": invalid_params_conf
    }

    response = client.post("/v1/configurator/", data=data, format="json")
    assert response.status_code == 400


def test_create_conf_using_API_with_invalid_fields(valid_base_conf):
    client = APIClient()
    data = {
        "base": valid_base_conf
    }

    response = client.post("/v1/configurator/", data=data, format="json")
    assert response.status_code == 400

















