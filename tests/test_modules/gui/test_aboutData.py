from gui.aboutData import versionString, licenses, developers, credits, description


def test_aboutData():
    assert versionString.__len__() > 0
    assert licenses.__len__() > 0
    assert developers.__len__() > 0
    assert credits.__len__() > 0
    assert description.__len__() > 0
