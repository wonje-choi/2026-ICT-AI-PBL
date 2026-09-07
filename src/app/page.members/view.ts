import { OnInit } from '@angular/core';
import { Service } from '@wiz/libs/portal/season/service';

export class Component implements OnInit {
    public loading: boolean = false;
    public members: any[] = [];

    public search: any = {
        text: "",
        role: ""
    };

    public roles: any[] = [
        { key: 'admin', label: '관리자' },
        { key: 'user', label: '회원' }
    ];

    public showInviteModal: boolean = false;
    public inviteData: any = { email: '', role: 'user' };

    constructor(public service: Service) { }

    public async ngOnInit() {
        await this.service.init();
        await this.service.auth.allow.role("admin", "/dashboard");
        await this.load();
    }

    public async load() {
        this.loading = true;
        await this.service.render();

        const { code, data } = await wiz.call("list", this.search);
        if (code === 200) {
            this.members = data || [];
        } else {
            this.members = [];
        }

        this.loading = false;
        await this.service.render();
    }

    public async filterByRole(role: string) {
        this.search.role = this.search.role === role ? "" : role;
        await this.load();
    }

    public async openInvite() {
        this.inviteData = { email: '', role: 'user' };
        this.showInviteModal = true;
        await this.service.render();
    }

    public async closeInvite() {
        this.showInviteModal = false;
        await this.service.render();
    }

    public async invite() {
        if (!this.inviteData.email) {
            await this.service.modal.error("이메일을 입력해주세요.");
            return;
        }

        const { code, data } = await wiz.call("invite", this.inviteData);
        if (code === 200) {
            await this.service.modal.success("멤버 계정이 생성되었습니다. 초기 비밀번호는 welcome1입니다.");
            this.showInviteModal = false;
            await this.load();
        } else {
            await this.service.modal.error(data?.message || data || "초대에 실패했습니다.");
        }
    }

    public async removeMember(member: any) {
        const res = await this.service.modal.show({
            title: "멤버 제거",
            message: `${member.name}님을 멤버에서 제거하시겠습니까?`,
            action: "제거",
            actionBtn: "error",
            status: "error"
        });
        if (!res) return;

        const { code, data } = await wiz.call("remove", { id: member.id });
        if (code === 200) {
            await this.load();
        } else {
            await this.service.modal.error(data?.message || data || "멤버를 제거하지 못했습니다.");
        }
    }

    public roleLabel(role: string) {
        return role === 'admin' ? '관리자' : '회원';
    }

    public roleClass(role: string) {
        return role === 'admin'
            ? 'bg-purple-100 text-purple-700'
            : 'bg-blue-100 text-blue-700';
    }
}
