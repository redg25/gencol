from gencol import Gencol

def test_position():
    test = Gencol('C:\\Users\\regis\\PycharmProjects\\gencol\\images')
    test.get_content()
    assert test.feature_pos('backgrounds',2).all_features['backgrounds'].position == 2
    assert test.feature_pos('backgrounds', 2).all_features['f1_eyes'].position == 1

