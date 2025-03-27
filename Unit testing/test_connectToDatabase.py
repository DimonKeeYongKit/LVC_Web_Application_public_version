import pytest
from connectToDatabase import *


@pytest.mark.connectToDatabase
def test_create_database_workbook():
    # test to create workbook
    result = create_crawler_workbook('Testing', 'Post', 'Facebook')
    assert result is True
    # test to create invalid workbook
    result = create_crawler_workbook('Testing', 'Post', 'Instagram')
    assert result is False


@pytest.mark.connectToDatabase
def test_load_content_workbook():
    # test to load content from exist workbook
    result = load_crawler_workbook('hello', 'Post', 'Facebook')
    assert type(result) is list
    # test to load content from not exist workbook
    result = load_crawler_workbook('thisfilenotexist', 'Post', 'Facebook')
    assert result is False
    # test to load content from invalid workbook
    result = load_crawler_workbook('hello', 'Post', 'Instagram')
    assert result is False


@pytest.mark.connectToDatabase
def test_load_full_workbook():
    # test to load exist workbook
    result = load_full_workbook('hello', 'Post', 'Facebook')
    assert type(result) is list
    # test to load not exist workbook
    result = load_full_workbook('thisfilenotexist', 'Post', 'Facebook')
    assert result is False
    # test to load invalid workbook
    result = load_full_workbook('hello', 'Post', 'Instagram')
    assert result is False


@pytest.mark.connectToDatabase
def test_load_lite_workbook():
    # test to load exist workbook
    result = load_lite_workbook('hello', 'Post', 'Facebook')
    assert type(result) is list
    # test to load not exist workbook
    result = load_lite_workbook('thisfilenotexist', 'Post', 'Facebook')
    assert result is False
    # test to load invalid workbook
    result = load_lite_workbook('hello', 'Post', 'Instagram')
    assert result is False


@pytest.mark.connectToDatabase
def test_check_database_workbook():
    # test to check exist workbook
    result = check_crawler_workbook('hello', 'Post', 'Facebook')
    assert result is True
    # test to check not exist workbook
    result = check_crawler_workbook('thisfilenotexist', 'Post', 'Facebook')
    assert result is False
    # test to check invalid workbook
    result = check_crawler_workbook('hello', 'Post', 'Instagram')
    assert result is False


@pytest.mark.connectToDatabase
def test_add_row_workbook():
    dataset = [['1452470259672174593', 'HELLO MY LOVES!!!! 😭❤️ https://t.co/nMFuiiksQY', '25-10-2021', '03:01:10',
      'https://twitter.com/i/web/status/1452470259672174593', '737528273152835585', 'minwonlogy', '25-10-2021',
                '11:01:11'], ['1452470259487703043', 'RT @yourrkycn: hello guyszz! I’m looking for #KyCine moots, I’m new babies her I decided to create a stan account to get updated with thei…',
                    '25-10-2021', '03:01:10', 'https://twitter.com/i/web/status/1452470259487703043',
                    '1323958288375951360', 'love_4kycine', '25-10-2021', '11:01:11'], ['1452470254689406983',
                                                                                       'RT @enhaPINS_: [HELP RT]\n\nHello if ever nahihirapan po kayo sa math assignments nyo, I am doing an "Assignment Commission" po. You can pay…',
                                                                                       '25-10-2021', '03:01:08',
                                                                                       'https://twitter.com/i/web/status/1452470254689406983',
                                                                                       '732549003934490626',
                                                                                       'BagsofRicci', '25-10-2021',
                                                                                       '11:01:11']]
    # test to add row into exist workbook
    result = add_row_workbook('testing', 'Post', 'Facebook', dataset)
    assert result is True
    # test to add row into not exist workbook
    result = add_row_workbook('thisfilenotexist', 'Post', 'Facebook', dataset)
    assert result is False
    # test to add row into invalid workbook
    result = add_row_workbook('hello', 'Post', 'Instagram', dataset)
    assert result is False


@pytest.mark.connectToDatabase
def test_delete_row_workbook():
    # test to delete exist row
    result = delete_row_workbook('tarconfessions', 'Post', 'Facebook', 2)
    assert result is True
    # test to delete no exist row
    result = delete_row_workbook('tarconfessions', 'Post', 'Facebook', 10000)
    assert result is False
    # test to delete row in no exist workbook
    result = delete_row_workbook('thisfilenotexist', 'Post', 'Facebook', 10)
    assert result is False
    # test to delete row in invalid workbook
    result = delete_row_workbook('hello', 'Post', 'Instagram', 10)
    assert result is False


@pytest.mark.connectToDatabase
def test_load_exist_postID():
    # test to load exist post id from exist workbook
    result = load_exist_postID('hello', 'Post', 'Facebook')
    assert type(result) is list
    # test to load exist post id from not exist workbook
    result = load_exist_postID('thisfilenotexist', 'Post', 'Facebook')
    assert result is False
    # test to load exist post id from invalid workbook
    result = load_exist_postID('hello', 'Post', 'Instagram')
    assert result is False
