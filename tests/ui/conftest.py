import os
import sys
import time
import signal
import logging
import subprocess
import psutil
import pytest
from appium import webdriver

from config import (
    APPIUM_SERVER_URL, 
    APP_PACKAGE,
    get_driver_options,
)
from pages.login_page import LoginPage


def pytest_collection_modifyitems(config, items):
    if os.getenv("CI") == "true":
        skip_device = pytest.mark.skip(reason="Skipping device tests in CI")
        for item in items:
            if "device" in item.keywords:
                item.add_marker(skip_device)


@pytest.fixture(scope="session")
def appium_server():
    if os.getenv("CI") == "true":
        yield
        return
    
    logging.info("[INIT] Appium 서버 실행 중...")

    appium_path = os.environ.get(
        "PATH_APPIUM",
        os.path.expandvars(r"%APPDATA%\npm\appium.cmd")
    )

    creationflags = (
        subprocess.CREATE_NEW_CONSOLE
        if sys.platform.startswith("win") 
        else 0
    )

    server = subprocess.Popen(
        [appium_path, "--allow-cors"], 
        creationflags=creationflags
    )
    
    logging.info("[INIT] Appium 서버 시작 성공")
    time.sleep(5)

    yield

    logging.info("[TEARDOWN] Appium 서버 중단 중...")

    try:
        server_pid = getattr(server, "pid", None)
        if server_pid and psutil.pid_exists(server_pid):
            if os.name == "nt":  # Windows
                subprocess.run(["taskkill", "/F", "/PID", str(server_pid), "/T"], check=True)
            else:  # Mac/Linux
                os.kill(server_pid, signal.SIGTERM)

            time.sleep(1)
            logging.info("[TEARDOWN] Appium 서버 정상 종료")
        else:
            logging.info("[WARN] Appium 서버가 이미 종료된 상태임")

    except Exception as e:
        logging.error(f"[ERROR] Appium 서버 종료 중 예외 발생: {e}")


@pytest.fixture(scope="session")
def driver(request, appium_server):
    if os.getenv("CI") == "true":
        yield None
        return

    if not any("device" in item.keywords for item in request.session.items):
        yield None
        return
    
    logging.info("[SETUP] Appium 드라이버 세션 생성 중...")

    driver = webdriver.Remote(APPIUM_SERVER_URL, options=get_driver_options())

    yield driver

    logging.info("[TEARDOWN] Appium 드라이버 세션 종료 중...")
    driver.quit()
    logging.info("[TEARDOWN] 드라이버 세션 종료 완료")
    

@pytest.fixture(autouse=True)
def reset_between_sets(request, driver):
    """테스트 데이터 세트(set_name) 변경 시 앱 재시작."""
    if request.node.get_closest_marker("device") is None:
        yield
        return
    
    callspec = getattr(request.node, "callspec", None)
    set_name = callspec.params.get("set_name") if callspec else None
    prev = getattr(request.session, "last_set_name", None)

    if set_name and prev != set_name:
        prev_label = prev if prev is not None else "INIT"
        logging.info(f"[RESET] 세트 변경 감지: {prev_label} → {set_name}")

        driver.terminate_app(APP_PACKAGE)
        driver.activate_app(APP_PACKAGE)
        time.sleep(5)

    if set_name:
        request.session.last_set_name = set_name

    yield


@pytest.fixture(scope="function")
def page(driver):
    return LoginPage(driver)


@pytest.fixture(scope="function", autouse=True)
def ensure_login_screen(request, page, reset_between_sets):
    """각 테스트 함수 실행 전 로그인 화면 상태를 보장하는 fixture."""
    if request.node.get_closest_marker("device") is None:
        yield
        return
    
    if not page.is_on_login_screen():
        page.navigate_to_login_screen()

    yield