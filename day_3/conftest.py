import json
from pytest import fixture

data_path = 'tests/test_data.json'


def load_test_data(path, key):
    with open(path) as data_file:
        data = json.load(data_file)
        return data[key]


@fixture(params=load_test_data(data_path,"names"))
def names(request):
    params = request.param
    return params


@fixture(params=load_test_data(data_path, "exclude_params"))
def exclude_params(request):
    params = request.param
    return params
