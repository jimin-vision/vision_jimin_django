PROFILE = {
    "name": "박지민",
    "headline": "전주비전대학교 컴퓨터정보과 1학년",
    "summary": "C, Python, Java를 다룰 수 있습니다.",
    "email": "vision202518015@gmail.com",
    "github": "https://github.com/jimin-vision",
    "resume": "",
}

PROJECTS = [
    {
        "name": "피그마",
        "summary": (
            "스마트팜 GUI의 정보 구조와 사용자 흐름을 정리하기 위해 Figma로 "
            "와이어프레임과 프로토타입을 제작했습니다. 화면 레이아웃과 주요 "
            "인터랙션 동선을 시각화해 개발 전에 흐름을 검증했습니다."
        ),
        "tech_stack": ["Figma", "Wireframe", "Prototype"],
        "link": "",
    },
    {
        "name": "스마트팜",
        "summary": (
            "AnyGrow2 보드와 PC를 pyserial로 연결해 센서 데이터를 수신하고 "
            "PyQt 데스크톱 GUI에 표시하는 모니터링/제어 프로그램을 구현했습니다. "
            "버튼/예약 입력 기반 제어 패킷을 구성해 보드로 전송하며 QThread/QTimer로 "
            "실시간 처리를 분리했습니다."
        ),
        "details": [
            "목적: 센서 -> 보드(AnyGrow2) -> 시리얼 통신 -> PC(Python GUI) 흐름으로 "
            "데이터를 모니터링하고, PC에서 보드로 제어 명령을 전송하는 스마트팜 통합 UI 제작.",
            "보드에서 올라오는 센서 데이터 수신/파싱 후 화면 표시.",
            "GUI 버튼 입력 기반 제어 패킷 생성 후 보드로 전송.",
            "JSON 기반 예약 스케줄링(예약 데이터 저장/로드 + 예약 실행 로직).",
            "QThread/QTimer 기반 비동기 처리로 UI 프리징 방지 및 실시간 갱신.",
            "Figma로 화면 구조/레이아웃/동선 설계(프로토타입으로 흐름 검증).",
        ],
        "highlights": [
            "PyQt 기반 데스크톱 GUI",
            "AnyGrow2 보드 연동(센서/제어)",
            "pyserial 시리얼 통신으로 데이터 송수신",
            "QThread/QTimer로 실시간 처리(화면 멈춤 방지)",
            "JSON 기반 예약 스케줄링 구현",
        ],
        "note": "발표/구성상 Python 파트는 본인 구현, Java 파트는 조원이 발표/구현.",
        "tech_stack": ["Python", "PyQt", "pyserial", "AnyGrow2", "Packet Protocol", "QThread/QTimer", "JSON"],
        "link": "",
    },
]

LANGUAGE_USAGE = []

WORK_USAGE = []
