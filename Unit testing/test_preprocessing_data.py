import pytest
from preprocessing_data import *


@pytest.mark.preprocessing_data
def test_cleanText():
    # test to remove tag
    assert cleanText('front @hello back') == 'front  back'
    # test to remove hashtag
    assert cleanText('front #hello back') == 'front  back'
    # test to remove hyperlink
    assert cleanText('front https://t.co/nMFuiiksQY back') == 'front  back'
    # test to remove next line
    assert cleanText('front \n\n back') == 'front  back'
    # test to remove 'RT'
    assert cleanText('front RT back') == 'front  back'
    # test to remove number
    assert cleanText('front 1234 back') == 'front  back'
    # test to remove '[OC]'
    assert cleanText('front [OC] back') == 'front  back'


@pytest.mark.preprocessing_data
def test_remove_emoji():
    # test to remove emoji
    assert remove_emoji('HELLO MY LOVES!!!! 😭❤') == 'HELLO MY LOVES!!!! '


@pytest.mark.preprocessing_data
def test_lowercase_and_punctuation_process():
    # test to lowercase the font
    assert lower_and_punctuation_process('HELLO MY LOVES!!!!') == 'hello my loves!!!!'
    # test to remove useless punctuation
    assert lower_and_punctuation_process('HELLO MY LOVES*!&!!$%!') == 'hello my loves!!!!'
