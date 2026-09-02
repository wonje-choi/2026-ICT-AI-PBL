# =============================================================================
# User Sub-Struct (사용자 비즈니스 로직)
# =============================================================================
# 사용 패턴:
#   struct = wiz.model("struct")
#   struct.user.authenticate("email@example.com", "hashed_password")
#   struct.user.get("user_id")
#   struct.user.list(text="검색어", role="admin")
#   struct.user.update_profile(user_id, name="새이름", mobile="010-...")
# =============================================================================

import datetime
import re
import bcrypt

class User:
    def __init__(self, core):
        self.core = core
        self.db = core.orm.use("user")

    def _hash_password(self, password):
        """비밀번호 bcrypt 해시"""
        if isinstance(password, str):
            password = password.encode('utf-8')
        return bcrypt.hashpw(password, bcrypt.gensalt()).decode('utf-8')

    def _check_password(self, password, hashed):
        """비밀번호 검증"""
        if isinstance(password, str):
            password = password.encode('utf-8')
        if isinstance(hashed, str):
            hashed = hashed.encode('utf-8')
        return bcrypt.checkpw(password, hashed)

    def authenticate(self, identifier, password):
        """아이디 또는 이메일과 비밀번호로 사용자를 인증합니다."""
        identifier = str(identifier or '').strip()
        if not identifier or not password:
            return None

        user = self.db.get(id=identifier.lower())
        if user is None:
            user = self.db.get(email=identifier.lower())
        if user is None:
            return None

        try:
            authenticated = self._check_password(password, user.get('password', ''))
        except (TypeError, ValueError):
            return None
        if authenticated is False:
            return None

        user.pop('password', None)
        return user

    def register(self, identifier, email, password, name):
        """회원가입 입력을 검증하고 로그인 가능한 사용자 계정을 생성합니다."""
        identifier = str(identifier or '').strip().lower()
        email = str(email or '').strip().lower()
        password = str(password or '')
        name = str(name or '').strip()

        if re.fullmatch(r'[a-z0-9]{4,32}', identifier) is None:
            raise ValueError("아이디는 영문 또는 숫자 4~32자로 입력해주세요.")
        if len(email) > 128 or re.fullmatch(r'[^\s@]+@[^\s@]+\.[^\s@]+', email) is None:
            raise ValueError("올바른 이메일 주소를 입력해주세요.")
        if not name or len(name) > 50:
            raise ValueError("닉네임은 1~50자로 입력해주세요.")
        if len(password) < 8 or len(password.encode('utf-8')) > 72:
            raise ValueError("비밀번호는 8자 이상, UTF-8 기준 72바이트 이하로 입력해주세요.")

        if self.db.get(id=identifier) is not None:
            raise ValueError("이미 사용 중인 아이디입니다.")
        if self.db.get(email=email) is not None:
            raise ValueError("이미 가입된 이메일입니다.")

        self.create(dict(
            id=identifier,
            email=email,
            password=password,
            name=name,
            role="user"
        ))
        return identifier

    def get(self, id=None):
        """사용자 단건 조회 (비밀번호 제외)

        Args:
            id: 사용자 ID

        Returns:
            dict 또는 None
        """
        user = self.db.get(id=id)
        if user:
            user.pop('password', None)
        return user

    def list(self, text="", role=""):
        """사용자 목록 조회

        Args:
            text: 이름/이메일 검색어
            role: 역할 필터

        Returns:
            list[dict]
        """
        kwargs = dict()
        like = None

        if role:
            kwargs['role'] = role
        if text:
            kwargs['name'] = text
            like = "name"

        rows = self.db.rows(
            orderby="created", order="ASC",
            like=like,
            **kwargs
        )
        # 비밀번호 필드 제거
        for r in rows:
            r.pop('password', None)
        return rows

    def create(self, data):
        """사용자 생성

        Args:
            data: {"email", "password", "name", "role"} dict

        Returns:
            생성된 사용자 ID
        """
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data['password'] = self._hash_password(data['password'])
        data['created'] = now
        data['updated'] = now
        if not data.get('role'):
            data['role'] = 'user'
        return self.db.insert(data)

    def update_profile(self, id, **fields):
        """프로필 업데이트 (name, mobile 등)

        Args:
            id: 사용자 ID
            **fields: 업데이트할 필드
        """
        fields['updated'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.db.update(fields, id=id)

    def change_password(self, id, current_password, new_password):
        """비밀번호 변경

        Args:
            id: 사용자 ID
            current_password: 현재 비밀번호 (평문)
            new_password: 새 비밀번호 (평문)

        Returns:
            bool (성공 여부)
        """
        user = self.db.get(id=id)
        if user is None:
            return False
        if not self._check_password(current_password, user.get('password', '')):
            return False
        hashed = self._hash_password(new_password)
        self.db.update(dict(
            password=hashed,
            updated=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ), id=id)
        return True

    def count(self, **kwargs):
        """사용자 수 조회"""
        return self.db.count(**kwargs) or 0

Model = User
