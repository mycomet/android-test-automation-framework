import copy
import pytest
import logging

from handlers.samsung_pass_handler import handle_samsung_pass
from data.login_data import login_case_sets


test_params = []
test_ids = []

for set_name, cases in login_case_sets:
    for case in cases:
        test_params.append((set_name, copy.deepcopy(case)))
        test_ids.append(f"{set_name}_case{case['case_id']}")


def login_flow(page, phone, password):
    """로그인 화면 진입 후 휴대폰 번호 로그인 전체 플로우 수행."""
    page.select_phone_login()
    handle_samsung_pass(page.driver)

    page.enter_login_credentials(phone, password)
    page.click_login_button()

    handle_samsung_pass(page.driver)

@pytest.mark.device
@pytest.mark.login
@pytest.mark.parametrize("set_name, case", test_params, ids=test_ids)
def test_login(driver, page, ensure_login_screen, set_name, case):
    """로그인 실패 시나리오 및 삼성패스 팝업 동작 검증."""
    
    raw_case_id = case["case_id"]
    
    case_id = f"{set_name.upper()}_CASE{raw_case_id}"
    phone, password = case["phone"], case["password"]
    expected_error = case["expected_error"]

    log_phone = f"****{phone[-4:]}" if phone else "없음"
    log_pw = "****" if password else "없음"
    logging.info(
        f"[START] {case_id} - {case['description']} "
        f"(전화번호: {log_phone}, 비밀번호: {log_pw})"
    )

    login_flow(page, phone, password)

    actual_error = page.get_login_error_message()

    if expected_error is not None:
        assert actual_error == expected_error
        logging.info(f"[VALIDATION] 에러 메시지 감지: '{actual_error}'")
    else:
        assert actual_error is None
        assert page.is_on_login_screen()

    logging.info(f"[RESULT][{case_id}] 테스트 완료")
