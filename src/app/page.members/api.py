struct = wiz.model("struct")

ALLOWED_ROLES = ["admin", "user"]


def list():
    text = wiz.request.query("text", "")
    requested_role = wiz.request.query("role", "")
    role = requested_role if requested_role in ALLOWED_ROLES else ""

    query_role = "" if requested_role == "user" else role
    members = struct.user.list(text=text, role=query_role)
    if requested_role == "user":
        members = [member for member in members if member.get("role") != "admin"]

    colors = [
        "bg-indigo-100 text-indigo-700",
        "bg-pink-100 text-pink-700",
        "bg-green-100 text-green-700",
        "bg-amber-100 text-amber-700",
        "bg-cyan-100 text-cyan-700",
        "bg-violet-100 text-violet-700",
    ]
    for i, member in enumerate(members):
        member["avatarColor"] = colors[i % len(colors)]
        member["joined"] = str(member.get("created", ""))[:10]
        member["role"] = "admin" if member.get("role") == "admin" else "user"

    wiz.response.status(200, members)


def invite():
    email = wiz.request.query("email", "").strip().lower()
    role = wiz.request.query("role", "user").strip()

    if not email:
        wiz.response.status(400, message="이메일을 입력해주세요.")
    if role not in ALLOWED_ROLES:
        wiz.response.status(400, message="허용되지 않은 역할입니다.")

    existing = struct.user.db.get(email=email)
    if existing:
        wiz.response.status(400, message="이미 등록된 사용자입니다.")

    struct.user.create(dict(
        email=email,
        password="welcome1",
        name=email.split("@")[0],
        role=role
    ))

    wiz.response.status(200)


def remove():
    member_id = wiz.request.query("id", "")
    if not member_id:
        wiz.response.status(400, message="ID가 필요합니다.")
    if member_id == wiz.session.get("id"):
        wiz.response.status(400, message="현재 로그인한 관리자 계정은 제거할 수 없습니다.")

    member = struct.user.get(member_id)
    if member is None:
        wiz.response.status(404, message="멤버를 찾을 수 없습니다.")

    struct.user.db.delete(id=member_id)
    wiz.response.status(200)
