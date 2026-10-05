def test_imports():
    import pages.login_page
    import config
    import data.login_data


def test_login_page_init():
    from pages.login_page import LoginPage

    class DummyDriver:
        pass

    page = LoginPage(DummyDriver())
    assert page is not None