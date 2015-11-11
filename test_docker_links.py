# Tests using pytest

from docker_links import DockerLinks


def test_all_links():
    links = DockerLinks()
    all_links = links.links()

    assert len(all_links) == 4
    assert 'test1' in all_links
    assert '132c2710a189' in all_links
    assert 'test3withlotofcharacters' in all_links
    assert 'test4' in all_links


def test_filtering():
    links = DockerLinks()
    test1 = links.links("test1")

    assert len(test1) == 1
    assert 'test1' in test1

    test2_and_3 = links.links("132c2710a189", "test3withlotofcharacters")

    assert len(test2_and_3) == 2
    assert '132c2710a189' in test2_and_3
    assert 'test3withlotofcharacters' in test2_and_3

    test4_and_5 = links.links("test4", "notexist")
    assert len(test4_and_5) == 1
    assert 'test4' in test4_and_5

    test5 = links.links("notexist")
    assert len(test5) == 0


def test_env():
    links = DockerLinks()
    all_links = links.links()

    assert all_links["test1"]["environment"]["FOO"] == "bar"
    assert all_links["test3withlotofcharacters"]["environment"]["FOO"] == "bar"


def test_ports():
    links = DockerLinks()

    ports = links('test1', '132c2710a189')

    assert ports['test1']["ports"]["800"]['protocol'] is 'tcp'
    assert ports['test1']["ports"]["8001"]['protocol'] is 'udp'
    assert ports['132c2710a189']["ports"]["800"]['protocol'] is 'udp'
    assert ports['132c2710a189']["ports"]["8001"]['protocol'] is 'tcp'
