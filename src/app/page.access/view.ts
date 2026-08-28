import { OnInit } from '@angular/core';
import { Service } from '@wiz/libs/portal/season/service';

export class Component implements OnInit {
    public view: string = 'login';
    public recoverMode: string = 'id';
    public passwordVisible: boolean = false;
    public registerPasswordVisible: boolean = false;
    public loginLoading: boolean = false;
    public errorMessage: string = '';
    public registerError: string = '';
    public recoveryError: string = '';
    public recoverySent: boolean = false;
    public fieldErrors: any = {};

    public data: any = {
        identifier: '',
        password: '',
        remember: false
    };

    public registerData: any = {
        identifier: '',
        email: '',
        password: '',
        passwordConfirm: '',
        nickname: '',
        terms: false,
        privacy: false,
        improvement: false
    };

    public recoveryData: any = {
        identifier: '',
        email: ''
    };

    constructor(public service: Service) { }

    public async ngOnInit() {
        await this.service.init();

        const authenticated = await this.service.auth.check();
        if (authenticated) {
            this.moveToAuthenticatedPage(this.service.auth.session?.role || '');
            return;
        }

        try {
            const rememberedId = localStorage.getItem('paperflow.rememberedId');
            if (rememberedId) {
                this.data.identifier = rememberedId;
                this.data.remember = true;
            }
        } catch (e) {
            // 저장소 사용이 제한된 브라우저에서도 로그인은 계속 동작합니다.
        }

        await this.service.render();
    }

    private moveToAuthenticatedPage(role: string) {
        location.href = role === 'admin' ? '/dashboard' : '/';
    }

    public async go(view: string) {
        this.view = view;
        this.errorMessage = '';
        this.registerError = '';
        this.recoveryError = '';
        this.recoverySent = false;
        this.fieldErrors = {};
        await this.service.render();
    }

    public async fillDemoAccount() {
        this.data.identifier = 'admin';
        this.data.password = '1234';
        this.data.remember = false;
        this.errorMessage = '';
        this.fieldErrors = {};
        await this.service.render();
    }

    public async togglePassword() {
        this.passwordVisible = !this.passwordVisible;
        await this.service.render();
    }

    public async toggleRegisterPassword() {
        this.registerPasswordVisible = !this.registerPasswordVisible;
        await this.service.render();
    }

    public async login() {
        this.errorMessage = '';
        this.fieldErrors = {};

        const identifier = String(this.data.identifier || '').trim();
        const password = String(this.data.password || '');

        if (!identifier) {
            this.fieldErrors.identifier = '아이디를 입력해주세요.';
        }
        if (!password) {
            this.fieldErrors.password = '비밀번호를 입력해주세요.';
        }
        if (Object.keys(this.fieldErrors).length > 0) {
            await this.service.render();
            return;
        }

        this.loginLoading = true;
        await this.service.render();

        const { code, data } = await wiz.call('login', {
            identifier: identifier,
            password: password,
            remember: this.data.remember
        });

        if (code === 200 && data?.authenticated === true) {
            try {
                if (this.data.remember) {
                    localStorage.setItem('paperflow.rememberedId', identifier);
                } else {
                    localStorage.removeItem('paperflow.rememberedId');
                }
            } catch (e) {
                // 로그인 상태 유지용 아이디 저장 실패는 인증을 막지 않습니다.
            }

            this.moveToAuthenticatedPage(data?.role || '');
            return;
        }

        this.loginLoading = false;
        this.errorMessage = data?.message || '로그인에 실패했습니다. 입력 정보를 확인해주세요.';
        await this.service.render();
    }

    public async register() {
        this.registerError = '';

        const identifier = String(this.registerData.identifier || '').trim();
        const nickname = String(this.registerData.nickname || '').trim();
        const email = String(this.registerData.email || '').trim();
        const password = String(this.registerData.password || '');

        if (identifier.length < 4) {
            this.registerError = '아이디는 영문 또는 숫자 4자 이상으로 입력해주세요.';
        } else if (!nickname) {
            this.registerError = '닉네임을 입력해주세요.';
        } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
            this.registerError = '올바른 이메일 주소를 입력해주세요.';
        } else if (password.length < 8) {
            this.registerError = '비밀번호는 8자 이상으로 입력해주세요.';
        } else if (password !== this.registerData.passwordConfirm) {
            this.registerError = '비밀번호가 서로 일치하지 않습니다.';
        } else if (!this.registerData.terms || !this.registerData.privacy) {
            this.registerError = '이용약관과 개인정보 수집 동의는 필수입니다.';
        }

        if (this.registerError) {
            await this.service.render();
            return;
        }

        await this.service.modal.show({
            title: '회원가입 정보 확인',
            message: '화면 프로토타입에서는 입력 흐름까지만 제공됩니다. 실제 가입 API 연결 시 서버 인증 후 계정이 생성됩니다.',
            cancel: false,
            action: '확인',
            actionBtn: 'success',
            status: 'success'
        });

        this.data.identifier = identifier;
        this.data.password = '';
        await this.go('login');
    }

    public async openRecovery(mode: string) {
        this.recoverMode = mode;
        this.recoveryData.identifier = mode === 'password' ? String(this.data.identifier || '').trim() : '';
        this.recoveryData.email = '';
        await this.go('recover');
    }

    public async setRecoveryMode(mode: string) {
        this.recoverMode = mode;
        this.recoveryError = '';
        this.recoverySent = false;
        await this.service.render();
    }

    public async submitRecovery() {
        this.recoveryError = '';
        this.recoverySent = false;

        const identifier = String(this.recoveryData.identifier || '').trim();
        const email = String(this.recoveryData.email || '').trim();

        if (this.recoverMode === 'password' && !identifier) {
            this.recoveryError = '아이디를 입력해주세요.';
        } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
            this.recoveryError = '가입할 때 사용한 이메일을 정확히 입력해주세요.';
        }

        if (!this.recoveryError) {
            this.recoverySent = true;
        }

        await this.service.render();
    }

    public async showLegal(type: string) {
        const documents: any = {
            privacy: {
                title: '개인정보처리방침',
                message: '계정 및 프로젝트 데이터는 서비스 제공에 필요한 범위에서만 처리하며, 품질 개선에는 사용자가 별도로 동의한 데이터만 사용합니다.'
            },
            terms: {
                title: '이용약관',
                message: '업로드한 논문의 이용 권한과 생성 결과의 공개 범위를 사용자가 직접 확인하고 관리하는 것을 원칙으로 합니다.'
            },
            copyright: {
                title: '저작권 안내',
                message: '원문 논문의 저작권과 인용 기준을 준수해야 하며, 비공개 프로젝트는 공개 데이터나 공유 영상으로 사용되지 않습니다.'
            }
        };
        const document = documents[type];

        await this.service.modal.show({
            title: document.title,
            message: document.message,
            cancel: false,
            action: '확인',
            actionBtn: 'success',
            status: 'success'
        });
    }
}
