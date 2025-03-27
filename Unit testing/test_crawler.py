import pytest
from crawler import *


@pytest.mark.crawler
def test_crawl_Facebook_post():
    # test to crawl Facebook page's post
    result, exist_count = crawl_Facebook_post('hello', 3)
    assert type(result) is list
    assert type(exist_count) is int
    assert len(result) + exist_count == 3
    # test to crawl not exist Facebook page's post
    result, exist_count = crawl_Facebook_post('doqwidoiqw', 3)
    assert result is False


@pytest.mark.crawler
def test_crawl_Reddit_post():
    # test to crawl Reddit page's post
    result, exist_count = crawl_Reddit_post('hello', 3)
    assert type(result) is list
    assert type(exist_count) is int
    assert len(result) + exist_count == 3
    # test to crawl not exist Reddit page's post
    result, exist_count = crawl_Reddit_post('doqwidoiqw', 3)
    assert result is False


@pytest.mark.crawler
def test_crawl_Twitter_post():
    # test to crawl Twitter page's post
    result, exist_count = crawl_Twitter_post('hello', 3)
    assert type(result) is list
    assert type(exist_count) is int
    assert len(result) + exist_count == 3
    # test to crawl not exist Twitter page's post
    result, exist_count = crawl_Twitter_post('doqwidoiqw', 3)
    assert result is False
