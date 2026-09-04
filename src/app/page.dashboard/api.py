import re
from urllib.parse import urlparse

struct = wiz.model("struct")


def _source_title(source_type, source_value, fallback):
    title = str(fallback or "").strip()
    if title:
        return title[:200]

    source_value = str(source_value or "").strip()
    if source_type == "url":
        parsed = urlparse(source_value)
        candidate = parsed.path.rstrip("/").split("/")[-1] or parsed.netloc
        candidate = re.sub(r"[-_]+", " ", candidate)
        return candidate[:200] or "새 논문"

    filename = source_value.rsplit("/", 1)[-1]
    filename = re.sub(r"\.[^.]+$", "", filename)
    return filename[:200] or "새 논문"


def prepare_script():
    """논문 출처를 바탕으로 편집 가능한 대본 초안을 생성한다."""
    source_type = wiz.request.query("source_type", "url").strip()
    source_value = wiz.request.query("source_value", "").strip()
    paper_title = wiz.request.query("paper_title", "").strip()
    audience = wiz.request.query("audience", "일반 독자").strip()
    duration = wiz.request.query("duration", "5분").strip()

    if source_type not in ["url", "file"]:
        wiz.response.status(400, message="올바른 입력 방식을 선택해주세요.")
    if not source_value:
        wiz.response.status(400, message="논문 주소 또는 파일을 입력해주세요.")
    if source_type == "url":
        parsed = urlparse(source_value)
        if parsed.scheme not in ["http", "https"] or not parsed.netloc:
            wiz.response.status(400, message="http 또는 https 형식의 논문 주소를 입력해주세요.")

    title = _source_title(source_type, source_value, paper_title)
    source_label = source_value if source_type == "url" else "업로드 파일: " + source_value
    content = f"""[논문 영상 대본 초안]

원문: {source_label}
대상 시청자: {audience}
예상 길이: {duration}

1. 오프닝
이 논문이 다루는 핵심 질문은 무엇일까요? 오늘은 ‘{title}’의 연구 배경과 의미를 알기 쉽게 살펴봅니다.

2. 연구 배경
이 연구가 시작된 문제와 기존 연구의 한계를 소개합니다. 원문을 확인해 핵심 용어와 선행 연구를 보완해주세요.

3. 연구 방법
연구 대상, 데이터, 실험 또는 분석 절차를 시청자가 이해하기 쉬운 순서로 설명합니다.

4. 핵심 결과
가장 중요한 결과를 3가지 이내로 정리하고, 수치와 도표의 의미를 정확히 확인해 반영합니다.

5. 해석과 한계
연구 결과가 갖는 의미와 함께 저자가 밝힌 한계, 과도하게 일반화하면 안 되는 지점을 설명합니다.

6. 마무리
핵심 내용을 한 문장으로 정리하고, 원문과 참고 자료 확인을 안내합니다.

[이용 안내]
이 초안은 원문 검토 전 구성안입니다. 사실·수치·인용을 반드시 원문과 대조하고, 공개 또는 영상 제작 전에 저작권과 이용 허가 범위를 직접 확인해야 합니다."""

    post_id = struct.post.create(dict(
        title=title + " 대본",
        content=content,
        category="논문 대본",
        status="draft"
    ))

    wiz.response.status(200, id=post_id, title=title + " 대본", content=content)
