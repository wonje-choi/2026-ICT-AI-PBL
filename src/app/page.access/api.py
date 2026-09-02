import hashlib
import hmac

session = wiz.model("portal/season/session").use()
struct = wiz.model("struct")

# 공개 시연 계정은 평문 비밀번호 대신 PBKDF2 결과만 서버 코드에서 비교합니다.
# 실제 배포에서는 환경변수/보안 저장소와 운영 인증 시스템으로 교체해야 합니다.
_DEMO_ADMIN_ID = "admin"
_DEMO_ADMIN_SALT = b"paperflow-demo-admin-v1"
_DEMO_ADMIN_PASSWORD_HASH = bytes.fromhex(
    "02567e9f40bf419fc1231728e73504a10b32c40e148a0dde21bd1ec9711ac242"
)


def _is_demo_admin(identifier, password):
    if identifier.lower() != _DEMO_ADMIN_ID:
        return False
    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        _DEMO_ADMIN_SALT,
        210000
    )
    return hmac.compare_digest(password_hash, _DEMO_ADMIN_PASSWORD_HASH)



def _register_account():
    identifier = wiz.request.query("identifier", "").strip()
    email = wiz.request.query("email", "").strip()
    password = wiz.request.query("password", "")
    name = wiz.request.query("nickname", "").strip()
    terms = wiz.request.query("terms", "false").lower() == "true"
    privacy = wiz.request.query("privacy", "false").lower() == "true"

    if terms is False or privacy is False:
        wiz.response.status(
            400,
            created=False,
            message="이용약관과 개인정보 수집 동의는 필수입니다."
        )

    try:
        user_id = struct.user.register(identifier, email, password, name)
    except ValueError as e:
        wiz.response.status(400, created=False, message=str(e))
    except Exception:
        wiz.response.status(
            500,
            created=False,
            message="회원가입 처리 중 오류가 발생했습니다. 잠시 후 다시 시도해주세요."
        )

    wiz.response.status(
        201,
        created=True,
        identifier=user_id,
        message="회원가입이 완료되었습니다."
    )


def login():
    if wiz.request.query("action", "login") == "register":
        _register_account()

    identifier = wiz.request.query("identifier", "").strip()
    password = wiz.request.query("password", "")
    remember = wiz.request.query("remember", "false") == "true"

    if not identifier or not password:
        wiz.response.status(
            200,
            authenticated=False,
            message="아이디와 비밀번호를 입력해주세요."
        )

    if _is_demo_admin(identifier, password):
        session.set(
            id="demo-admin",
            email="admin@demo.paperflow.local",
            name="시연 관리자",
            role="admin",
            demo=True,
            remember=remember
        )
        wiz.response.status(
            200,
            authenticated=True,
            role="admin",
            redirect="/dashboard",
            demo=True
        )

    try:
        user = struct.user.authenticate(identifier, password)
    except Exception:
        user = None

    if user is None:
        wiz.response.status(
            200,
            authenticated=False,
            message="아이디 또는 비밀번호가 올바르지 않습니다."
        )

    session.set(
        id=user["id"],
        email=user["email"],
        name=user["name"],
        role=user["role"],
        remember=remember
    )
    redirect = "/dashboard" if user["role"] == "admin" else "/"
    wiz.response.status(
        200,
        authenticated=True,
        role=user["role"],
        redirect=redirect,
        demo=False
    )


def register():
    _register_account()
