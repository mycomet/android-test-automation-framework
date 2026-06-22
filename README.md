# Android Mobile Test Automation Framework (Appium + Pytest)

[![CI](https://img.shields.io/github/actions/workflow/status/mycomet/android-test-automation-framework/test.yml?style=for-the-badge&label=CI)](https://github.com/mycomet/android-test-automation-framework/actions)

![Python](https://img.shields.io/badge/python-3776AB.svg?style=for-the-badge&logo=python&logoColor=white)
![Android](https://img.shields.io/badge/android-3DDC84.svg?style=for-the-badge&logo=android&logoColor=white)
![Appium](https://img.shields.io/badge/appium-EE376D.svg?style=for-the-badge&logo=appium&logoColor=white)
![Pytest](https://img.shields.io/badge/pytest-0A9EDC.svg?style=for-the-badge&logo=pytest&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/github%20actions-2671E5.svg?style=for-the-badge&logo=githubactions&logoColor=white)
![Allure](https://img.shields.io/badge/allure-FF6C37.svg?style=for-the-badge)

Appium과 Pytest 기반의 Android 모바일 테스트 자동화 프레임워크로, Page Object Model(POM) 아키텍처를 적용하여 유지보수성과 확장성을 고려해 설계했습니다.

**'토스플레이스(Toss POS)' 앱의 로그인**을 테스트 대상으로 하여, 삼성패스 팝업 처리와 CI 인프라 연동을 구현한 테스트 자동화 포트폴리오입니다.

## 🚀 테스트 리포트
  - [🧪 CI 리포트](https://mycomet.github.io/android-test-automation-framework/ci/) — *GitHub Actions 환경에서 수행된 CI 스모크 테스트 결과*
  - [📱 모바일 리포트](https://mycomet.github.io/android-test-automation-framework/mobile/) — *실제 단말 연동 기반의 검증 시나리오 결과*

---

## ⚠️ 참고 사항
본 프로젝트는 **토스포스 앱의 이전 버전을 기준으로 구현 및 테스트가 완료**되었습니다. 
현재 앱 버전과 테스트 구현 시점의 로그인 프로세스 및 UI 레이아웃 차이로 인해, 최신 버전의 앱에서는 테스트 시나리오가 원래 구현대로 동작하지 않을 수 있습니다.

그러나 본 프레임워크는 **POM** 구조로 설계하여 전체 테스트 스크립트를 재작성할 필요 없이, 변경된 UI에 대해 Page Object 레이어를 부분적으로 업데이트하면 유지보수가 가능함을 전제로 합니다.

---

## 🎯 프로젝트 목적 및 핵심 설계 전략

본 프로젝트는 모든 서비스 앱의 공통 기능인 **로그인**을 기준으로 하여, 특정 앱이나 UI 버전에 강하게 종속되지 않고 유사한 로그인 플로우를 가진 안드로이드 앱에서 재사용 가능한 구조를 설계하는 데 초점을 맞추었습니다.

- **사전조건 격리 제어(`conftest.py`)**
  - 앱 실행 시, 첫 화면에서 로그인 화면으로의 진입까지의 전처리 과정을 독립 제어하여 일관된 테스트 시작 지점을 보장

- **유지보수 최적화(POM 구조)**
  - UI가 변경되더라도 시나리오 수정 없이 해당 페이지 객체 레이어를 업데이트하여 유지보수 가능

- **예외 핸들링(Samsung Pass 팝업 대응)**
  - 로그인 시도 시 발생하는 Samsung Pass 로그인 팝업을 실시간 감지·해제하는 독립형 핸들러 구현

- **환경 제약 극복(Hybrid CI)**
  - `pytest.mark.device` 마커를 활용하여 CI 스모크 테스트와 실단말 통합 테스트의 실행 범위 분리

---

## 📌 테스트 환경 및 대상

- **대상 애플리케이션:** 토스플레이스(Toss POS) Android 앱
- **계정 및 디바이스:** 가맹점 테스트 계정 및 Android 디바이스 / GitHub Actions 가상 러너(CI)

---

## 🛠️ 사용 기술 및 환경

- **Language:** Python
- **Automation Framework:** Appium, Selenium WebDriver
- **Mobile Driver:** Android UIAutomator2
- **Test Runner:** Pytest
- **CI Pipeline:** GitHub Actions
- **Test Report:** Allure Report (with GitHub Pages Deployment)

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
│   └── login_page.py               # 로그인 화면의 UI 엘리먼트 및 사용자 액션 정의
│
├── tests/
│   ├── conftest.py                 # Appium 드라이버 및 테스트 사전조건(Precondition) 관리
│   ├── test_login.py               # 실단말 기반 주요 통합 검증 시나리오 스크립트
│   └── test_smoke.py               # CI 환경용 스모크 테스트
│
├── config.py                       # Appium 드라이버 및 실행 환경 설정 관리
├── pytest.ini                      # Pytest 실행 옵션 및 커스텀 마커 정의
├── requirements.txt                # 프로젝트 의존성 패키지 명세
└── README.md
```

---

## 🔄 테스트 흐름

Pytest 세션이 기동되면 `conftest.py`가 드라이버를 초기화하고 로그인 화면으로의 안정적인 진입(Precondition)을 먼저 보장합니다. 

이후 준비된 테스트 데이터 순서에 따라 데이터 주도 테스팅(DDT)을 순차적으로 수행합니다.

```text
    <테스트 세션 시작>
          │
          ▼
       <앱 실행>
          │
          ▼
  <로그인 화면으로 이동> 
          │
          ▼
  <휴대폰 번호 로그인 선택>
          │
          ▼
  <Samsung Pass 팝업 취소 (발생 시)>
          │
          ▼
  <로그인 인증 정보 입력>
          │
          ▼
    <로그인 버튼 클릭>
          │
          ▼
  <최종 결과 검증 및 종료>
```

---

## ✅ 테스트 시나리오

`@pytest.mark.parametrize`를 활용한 데이터 주도 테스팅(DDT) 기법을 적용하여, 하나의 스크립트 안에서 아래의 필수 유효성 검사(Validation) 실패 흐름들을 순차적으로 검증합니다.

| ID | 테스트 시나리오 | 기대 결과 |
| --- | --- | --- |
| **CASE 1** | 로그인 정보 전체 미입력 상태로 시도 | 로그인 차단 및 현재 로그인 페이지 유지 상태 검증 |
| **CASE 2** | 휴대폰 번호만 입력 후 시도 | 로그인 차단 및 현재 로그인 페이지 유지 상태 검증 |
| **CASE 3** | 비밀번호만 입력 후 시도 | 로그인 차단 및 현재 로그인 페이지 유지 상태 검증 |
| **CASE 4** | 잘못된 로그인 정보 입력 후 시도 | 입력창 하단 에러 텍스트 `"ID를 확인해 주세요"` 일치 검증 |

---

## ⚙️ 실행 환경 최적화 전략

단말 연동이 불가능한 CI(GitHub Actions) 환경과 실제 단말 로컬 테스트 환경의 리소스 최적화를 위해 Pytest 커스텀 마커를 기반으로 실행 범위를 분리했습니다.

- **`@pytest.mark.device`**
  - 실제 Android 단말 연결이 필요한 통합 테스트

- **Non-marked 테스트 (마커 없음)**
  - CI 환경에서 실행되는 스모크 테스트

```bash
# 1. 가상 가속 빌드 환경용 가벼운 CI 스모크 테스트 수행
$ pytest -m "not device"

# 2. 로컬 실단말 환경 기반 전체 모바일 통합 검증 시나리오 수행 (물리 단말 연결 필요)
$ pytest -m device

# 3. 상세 디버깅 모드로 전체 테스트 실행
$ pytest -v
```

---

## 🤖 CI 파이프라인 및 리포트 자동화

본 프로젝트는 GitHub Actions와 Allure Report를 활용하여 지속적인 검증 및 테스트 리포트 자동화를 지원합니다.

- **지속적 통합 (CI)**  
  - `main` 브랜치에 코드가 Push되거나 Pull Request가 생성되면 GitHub Actions 워크플로우가 자동으로 실행
  - CI 환경에서는 실제 Android 단말 사용이 불가능하므로 `pytest -m "not device"`만 수행하여 기본적인 코드 변경 사항을 검증

- **리포트 배포**  
  - 테스트 결과는 Allure Report로 생성되며, GitHub Pages를 통해 배포
  - 배포 경로
    - `/ci` : GitHub Actions에서 자동 생성된 CI 리포트
    - `/mobile` : 실제 단말 테스트 후 수동 배포한 모바일 리포트

이를 통해 CI 검증 결과와 실제 단말 테스트 결과를 분리하여 관리할 수 있습니다.

---

## 📄 실행 로그 예시
테스트 단계별 진행 상황을 로그로 기록하여 실행 흐름을 추적할 수 있도록 했습니다.

```text
2026-03-12 16:00:21 [INFO] [RESET] 세트 변경 감지: INIT → set1
2026-03-12 16:00:26 [INFO] [START] SET1_CASE1 - 로그인 정보 미입력
2026-03-12 16:00:29 [INFO] [RESULT][SET1_CASE1] 테스트 완료
```

```text
2026-03-12 16:01:03 [INFO] [START] SET1_CASE4 - 잘못된 계정 정보 입력
2026-03-12 16:01:08 [INFO] [VALIDATION] 에러 메시지 감지: 'ID를 확인해 주세요'
2026-03-12 16:01:10 [INFO] [RESULT][SET1_CASE4] 테스트 완료
```

## 🚧 향후 개선 계획

- 실패 시 자동 스크린샷 및 Logcat 수집 기능 추가
- Allure 리포트 메타데이터 고도화