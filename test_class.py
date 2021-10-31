from gencol import Gencol,Feature
import pytest

# def test_position():
#     test = Gencol('C:\\Users\\regis\\PycharmProjects\\gencol\\images')
#     test.get_content()
#     assert test.feature_pos('backgrounds',2).all_features['backgrounds'].position == 2
#     assert test.feature_pos('backgrounds', 2).all_features['eyes'].position == 1

def test_position():
    test = Gencol('C:\\Users\\regis\\PycharmProjects\\gencol\\images')
    test.get_content()
    f1 = test.get_feature('mouths')
    f1.position = 1
    assert test.all_features['eyes'].position == 3
    assert test.all_features['mouths'].position == 1
    assert test.all_features['backgrounds'].position == 2
    f2 = test.get_feature('eyes')
    f2.position = 1
    assert test.all_features['eyes'].position == 1
    assert test.all_features['mouths'].position == 2
    assert test.all_features['backgrounds'].position == 3

def test_mandatory():
    test = Gencol('C:\\Users\\regis\\PycharmProjects\\gencol\\images')
    test.get_content()
    assert test.mandatory('backgrounds').all_features['backgrounds'].mandatory == True
    assert test.mandatory('backgrounds',set=False).all_features['backgrounds'].mandatory == False

def test_get_image():
    test = Gencol('C:\\Users\\regis\\PycharmProjects\\gencol\\images')
    test.get_content()
    assert test.get_image('eyes','eyes1') == test.all_features['eyes'].all_images['eyes1']

def test_get_feature():
    test = Gencol('C:\\Users\\regis\\PycharmProjects\\gencol\\images')
    test.get_content()
    assert test.get_feature('eyes') == test.all_features['eyes']

def test_find_position():
    ltest1 = [1,2,2,3]
    ltest2 = [1, 2, 3, 3]
    ltest3 = [1, 2, 2, 4]
    ltest4 = [1,2,3,4]
    assert Feature.find_empty_position(ltest1,4) == 4
    assert Feature.find_empty_position(ltest2,4) == 4
    assert Feature.find_empty_position(ltest3,3) == 3
    assert Feature.find_empty_position(ltest4,3) == 3