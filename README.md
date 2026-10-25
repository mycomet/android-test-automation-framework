# Android UI & API Test Automation Framework (Appium + Pytest)

[![CI](https://img.shields.io/github/actions/workflow/status/mycomet/android-test-automation-framework/test.yml?style=for-the-badge&label=CI)](https://github.com/mycomet/android-test-automation-framework/actions)

![Python](https://img.shields.io/badge/python-3776AB.svg?style=for-the-badge&logo=python&logoColor=white)
![Android](https://img.shields.io/badge/android-3DDC84.svg?style=for-the-badge&logo=android&logoColor=white)
![Appium](https://img.shields.io/badge/appium-EE376D.svg?style=for-the-badge&logo=appium&logoColor=white)
![Pytest](https://img.shields.io/badge/pytest-0A9EDC.svg?style=for-the-badge&logo=pytest&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/github%20actions-2671E5.svg?style=for-the-badge&logo=githubactions&logoColor=white)
![Allure](https://img.shields.io/badge/allure-FF6C37.svg?style=for-the-badge)

Appium과 Pytest 기반의 Android 모바일 테스트 자동화 프레임워크입니다. POM(Page Object Model) 디자인 패턴을 적용하여 유지보수성과 확장성을 고려하여 설계했습니다.

프레임워크의 동작과 테스트 자동화 구현을 보여주기 위해 **'토스플레이스(Toss POS)' 앱의 로그인 기능**을 UI 테스트 대상으로 선정하고, Samsung Pass 팝업 처리 및 CI 연동을 구현했습니다. 이후 WireMock 기반의 API 테스트 자동화 영역까지 확장했습니다.

---

## 📌 프로젝트 개발 이력

- V1.0 Android UI 테스트 자동화 프레임워크 구축
- V2.0 WireMock 기반 API 테스트 자동화 확장

---

## 🚀 테스트 리포트
  - [🧪 CI 리포트](https://mycomet.github.io/android-test-automation-framework/ci/) — *GitHub Actions 환경에서 수행된 CI 스모크 테스트 결과*
  - [📱 모바일 리포트](https://mycomet.github.io/android-test-automation-framework/mobile/) — *실제 단말 연동 기반의 검증 시나리오 결과 (구 버전 앱 기준)*

---

## ⚠️ 참고 사항
본 프로젝트는 **Toss Pos 앱의 이전 버전**을 기준으로 구현 및 테스트가 완료되었습니다.
현재 앱 버전과 테스트 구현 시점의 로그인 프로세스 및 UI 레이아웃 차이로 인해 최신 버전에서는 기존 테스트 시나리오가 의도대로 동작하지 않을 수 있습니다.

API 자동화는 토스플레이스의 실제 내부 API가 아닌 별도로 정의한 테스트용 Login API 계약을 대상으로 구현하였습니다.

---

## 🎯 프로젝트 목적 및 핵심 설계 전략

본 프로젝트는 유지보수성과 확장성을 고려한 Android 모바일 테스트 자동화 프레임워크 구축을 목적으로 합니다. POM 디자인 패턴을 적용하여 UI 요소와 테스트 로직을 분리하고, 새로운 테스트 시나리오와 검증 영역을 유연하게 추가할 수 있는 구조를 만드는 데 초점을 맞췄습니다.

추가로 API 테스트 자동화 영역까지 확장하여 UI와 API를 독립적으로 검증하고, Mock 환경을 활용해 다양한 API 응답 시나리오를 확인할 수 있도록 구성했습니다.


**1. UI 테스트 자동화**
  - **테스트 사전조건 관리(`conftest.py`)**
    - 앱 실행부터 로그인 화면 진입까지의 공통 준비 절차를 Fixture로 관리하여 테스트 시작 조건을 일관되게 유지
  - **UI 요소와 테스트 로직 분리(POM)**
    - UI 요소와 테스트 로직을 분리하여, UI 또는 테스트 흐름 변경 발생 시 수정 범위를 구분하고 유지보수성을 높일 수 있도록 설계
  - **예외 핸들링(Samsung Pass 팝업 대응)**
    - Samsung Pass 팝업을 감지하고 발생 시 해제하는 핸들러 구현하여 팝업 발생 유무에 따른 테스트 흐름을 제어
  - **CI와 실단말 테스트 분리(Hybrid CI)**
    - `pytest.mark.device` 마커를 활용하여 CI에서 실행할 스모크 테스트와 실제 단말이 필요한 테스트를 구분

**2. API 테스트 및 Mock 환경**
  - **API 테스트 자동화**
    - Pytest와 Requests를 활용하여 테스트용 Login API 요청 및 응답을 자동으로 검증
  - **HTTP 상태 코드 검증**
    - 정상 응답(200), 요청 오류(400), 인증 실패(401), 서버 내부 오류(500)를 시나리오별로 검증
  - **Response Body 검증**
    - `resultType`, `error.errorCode`, `error.reason` 등 주요 필드를 검증
  - **API Mock 환경 구성**
    - WireMock으로 요청 조건별 응답 시나리오 구성하여 실제 백엔드 서버에 의존하지 않는 API 테스트 환경 구축
  - **서버 오류 응답 시나리오 검증**
    - 테스트 전용 헤더를 이용하여 WireMock에서 500 응답을 반환하는 시나리오를 호출하고 오류 응답을 검증

---

## 📌 테스트 환경 및 대상
**1. UI 테스트**
- **테스트 대상:** 토스플레이스(Toss POS) Android 앱의 로그인 기능
- **실행 환경:** Android 디바이스 및 GitHub Actions 가상 러너 

**2. API 테스트**
- **테스트 대상**: 프로젝트에서 정의한 테스트용 Login API 명세
- **Mock 서버:** WireMock 3.13.2 (localhost:8080)

---

## 🛠️ 사용 기술 및 환경

- **Language:** Python
- **UI Automation:** Appium, Selenium WebDriver, Android UIAutomator2
- **API Testing:** Requests
- **API Mocking:** WireMock
- **Test Runner:** Pytest
- **CI:** GitHub Actions
- **Test Report:** Allure Report
- **Report Hosting:** GitHub Pages

---

## 📁 프로젝트 디렉토리 구조

```text
Tossplace_Automation_V2
│
├── data/
│   └── login_data.py               # 파라미터화(DDT) 테스트용 로그인 시나리오 데이터 관리
│
├── handlers/
│   └── samsung_pass_handler.py     # Samsung Pass 팝업 감지 및 예외 처리
│
├── pages/
│   ├── base_page.py                # 공통 UI 액션 및 Explicit Wait 기능 제공
│   └── login_page.py               # 로그인 화면의 UI 요소 및 사용자 액션 정의
│
├── mocks/
│   └── mappings/
│       ├── login_200.json
│       ├── login_400_both_missing.json
│       ├── login_400_password_missing.json
│       ├── login_400_phone_missing.json
│       ├── login_401.json
│       ├── login_500.json
│
├── tests/
│   ├── ui/
│   │   ├── conftest.py             # Appium 드라이버 및 테스트 사전조건(Precondition) 
│   │   ├── test_login.py           # 실단말 기반 주요 통합 검증 시나리오 스크립트
│   │   └── test_smoke.py           # CI 환경용 스모크 테스트
│   │
│   └── api/ 
│       └── test_login_api.py       # Login API 자동화 테스트
│
├── config.py                       # Appium 드라이버 및 실행 환경 설정 관리
├── pytest.ini                      # Pytest 실행 옵션 및 커스텀 마커 정의
├── requirements.txt                # 프로젝트 의존성 패키지 명세
└── README.md
```

---

## 🔌 API Mock 구조

WireMock으로 Mock 서버를 구성하고, 실제 Tossplace 내부 로그인 API 대신 테스트용 로그인 API 명세를 정의하여 요청 조건별 응답 시나리오를 구현했습니다.

### Request 예시

POST /api/login 
Content-Type: application/json

```
{
  "phone": "01012345678",
  "password": "test1234"
}
```

## ✅ UI 테스트 시나리오

`@pytest.mark.parametrize`를 활용한 데이터 주도 테스팅(DDT) 기법을 적용하여 로그인 입력 조건별 실패 흐름들을 순차적으로 검증합니다.

| ID | 테스트 시나리오 | 기대 결과 |
| --- | --- | --- |
| **CASE 1** | 로그인 정보 전체 미입력 상태로 시도 | 로그인 차단 및 현재 로그인 페이지 유지 상태 검증 |
| **CASE 2** | 휴대폰 번호만 입력 후 시도 | 로그인 차단 및 현재 로그인 페이지 유지 상태 검증 |
| **CASE 3** | 비밀번호만 입력 후 시도 | 로그인 차단 및 현재 로그인 페이지 유지 상태 검증 |
| **CASE 4** | 잘못된 로그인 정보 입력 후 시도 | 입력창 하단 에러 텍스트 `"ID를 확인해 주세요"` 일치 검증 |

---

## 🧪 API 테스트 시나리오

WireMock으로 구성한 Mock 응답을 활용하여 다양한 HTTP 상태 코드 및 응답 데이터 검증 시나리오를 수행합니다.

| ID         | HTTP Status | 테스트 시나리오           | 주요 검증                      |
| ---------- | ----------: | ------------------ | -------------------------- |
| **CASE 1** |     **200** | 정상적인 전화번호와 비밀번호 입력 | `resultType`, `success` 검증 |
| **CASE 2** |     **400** | 전화번호와 비밀번호 모두 미입력  | `errorCode`, `reason` 검증   |
| **CASE 3** |     **400** | 전화번호 입력 / 비밀번호 미입력 | `errorCode`, `reason` 검증   |
| **CASE 4** |     **400** | 전화번호 미입력 / 비밀번호 입력 | `errorCode`, `reason` 검증   |
| **CASE 5** |     **401** | 잘못된 로그인 정보 입력      | `errorCode`, `reason` 검증   |
| **CASE 6** |     **500** | 서버 내부 오류 상황 재현     | `errorCode`, `reason` 검증   |

### 500 Server Error 재현

일반적인 로그인 데이터와 서버 내부 오류를 분리하기 위해 테스트 전용 Header를 사용했습니다.

```http
X-Mock-Scenario: server-error
```

이를 통해 특정 전화번호나 비밀번호를 입력해야만 500 오류가 발생하는 방식이 아니라, **서버 오류라는 테스트 조건 자체를 명시적으로 제어**할 수 있도록 구성했습니다.

> `X-Mock-Scenario`는 실제 서비스 API의 Header가 아니라 본 프로젝트의 WireMock 테스트 환경에서만 사용하는 Mock 제어용 Header입니다.

---

## ⚙️ 테스트 실행 방법

**1. UI 테스트**

실제 Android 단말과 Appium 환경이 필요합니다.

- **실단말 테스트 제외**
```bash
$ pytest -m "not device"
```

- **실단말 테스트**
```bash
$ pytest -m device
```

**2. API 테스트**

먼저 별도 터미널에서 WireMock 서버를 실행합니다.
```bash
$ java -jar .\wiremock-standalone-3.13.2.jar --root-dir .\mocks
```
WireMock 실행 후 API 테스트를 수행합니다.
```bash
$ pytest tests/api/ -v
```

**3. 전체 테스트**

WireMock 서버와 필요한 UI 테스트 환경을 준비한 상태에서 실행합니다.
```bash
$ pytest -v
```

---

## 🤖 CI 파이프라인 및 리포트 자동화

GitHub Actions를 활용해 코드 Push 및 Pull Request 시 CI 테스트를 실행하고, Allure Report를 GitHub Pages에 배포합니다.

- **CI 리포트**: GitHub Actions에서 실행한 스모크 테스트 결과
- **모바일 리포트**: 실제 Android 단말에서 수행한 UI 테스트 결과(구 버전 앱 기준)

CI 환경에서는 실단말이 필요한 테스트를 제외하여 기본적인 테스트를 수행하며, 실제 단말 테스트 결과는 별도로 관리합니다.
