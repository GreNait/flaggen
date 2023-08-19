import pytest

from flaggen.feature_flag import feature_flag
from flaggen.feature_schema import Feature


def stub_func(response=True, option=None) -> bool:
    if option:
        return option

    return response


def test_name_feature():
    test_function = feature_flag(activation="off", name="test")
    test_function = test_function(stub_func)

    assert test_function.feature_name == "test"

    with pytest.raises(NotImplementedError):
        test_function()

    test_function.clean()


def test_name_feature_two_methods():
    test_function = feature_flag(activation="off", name="test")
    test_function = test_function(stub_func)

    test_function_2 = feature_flag(name="test")
    test_function_2 = test_function_2(stub_func)

    assert test_function_2.feature_name == "test"

    with pytest.raises(NotImplementedError):
        test_function_2()

    test_function.clean()
    test_function_2.clean()


def test_registere_features_deactive():
    test_function = feature_flag(activation="off", name="test")
    test_function = test_function(stub_func)

    assert (
        Feature(**{"name": "test", "activation": "off"})
        in test_function.registered_features
    )
    assert test_function.feature_active == "off"

    test_function_2 = feature_flag(name="test")
    test_function_2 = test_function_2(stub_func)

    assert test_function_2.feature_active == "off"
    assert (
        Feature(**{"name": "test", "activation": "off"})
        in test_function_2.registered_features
    )
    assert len(test_function.registered_features) == 1

    test_function.clean()
    test_function_2.clean()


def test_registere_features_active():
    test_function = feature_flag(activation="on", name="test")
    test_function = test_function(stub_func)

    assert (
        Feature(**{"name": "test", "activation": "on"})
        in test_function.registered_features
    )
    assert test_function.feature_active == "on"

    test_function_2 = feature_flag(name="test")
    test_function_2 = test_function_2(stub_func)

    assert test_function_2.feature_active == "on"
    assert (
        Feature(**{"name": "test", "activation": "on"})
        in test_function_2.registered_features
    )
    assert len(test_function.registered_features) == 1

    test_function.clean()
    test_function_2.clean()


def test_name_feature_two_methods_active():
    test_function = feature_flag(activation="on", name="test")
    test_function = test_function(stub_func)

    test_function_2 = feature_flag(name="test")
    test_function_2 = test_function_2(stub_func)

    assert test_function()
    assert test_function_2()

    test_function.clean()
    test_function_2.clean()


def test_two_different_feature_names():
    test_function = feature_flag(activation="on", name="test")
    test_function = test_function(stub_func)

    test_function_2 = feature_flag(name="test2")
    test_function_2 = test_function_2(stub_func)

    assert test_function.feature_name == "test"
    assert test_function.feature_active == "on"
    assert test_function_2.feature_name == "test2"
    assert test_function_2.feature_active == "off"
    assert len(test_function_2.registered_features) == 2

    test_function.clean()
    test_function_2.clean()


def test_two_methods_one_feature_as_decorator():
    @feature_flag("off", name="test")
    def test_method_1():
        return True

    @feature_flag(name="test")
    def test_method_2():
        return True

    assert test_method_1.feature_active == "off"
    assert test_method_2.feature_active == "off"
    assert len(test_method_2.registered_features) == 1

    with pytest.raises(NotImplementedError):
        test_method_1()

    with pytest.raises(NotImplementedError):
        test_method_2()

    test_method_1.clean()
    test_method_2.clean()


def test_two_methods_one_feature_as_decorator_active():
    @feature_flag("on", name="test")
    def test_method_1():
        return True

    @feature_flag(name="test")
    def test_method_2():
        return True

    assert test_method_1.feature_active == "on"
    assert test_method_2.feature_active == "on"
    assert len(test_method_2.registered_features) == 1

    assert test_method_1()
    assert test_method_2()

    test_method_1.clean()
    test_method_2.clean()


def test_two_methods_two_feature_as_decorator():
    @feature_flag("off", name="test")
    def test_method_1():
        return True

    @feature_flag(name="test2")
    def test_method_2():
        return True

    assert test_method_1.feature_active == "off"
    assert test_method_2.feature_active == "off"
    assert len(test_method_2.registered_features) == 2

    with pytest.raises(NotImplementedError):
        test_method_1()

    with pytest.raises(NotImplementedError):
        test_method_2()

    test_method_1.clean()
    test_method_2.clean()


def test_two_methods_one_feature_single_response():
    @feature_flag("off", name="test", response="test_method_1")
    def test_method_1():
        return True

    @feature_flag(name="test")
    def test_method_2():
        return True

    assert test_method_1() == "test_method_1"

    with pytest.raises(NotImplementedError):
        test_method_2()

    test_method_1.clean()
    test_method_2.clean()


def test_two_methods_one_feature_both_response():
    @feature_flag("off", name="test", response="test_method_1")
    def test_method_1():
        return True

    @feature_flag(name="test", response="test_method_2")
    def test_method_2():
        return True

    assert test_method_1() == "test_method_1"
    assert test_method_2() == "test_method_2"

    test_method_1.clean()
    test_method_2.clean()