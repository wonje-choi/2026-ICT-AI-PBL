import { OnInit } from '@angular/core';
import { Service } from '@wiz/libs/portal/season/service';

export class Component implements OnInit {
    public sourceType: 'url' | 'file' = 'url';
    public sourceUrl: string = '';
    public selectedFile: File | null = null;
    public paperTitle: string = '';
    public audience: string = '일반 독자';
    public duration: string = '5분';
    public preparing: boolean = false;
    public result: any = null;

    constructor(public service: Service) { }

    public async ngOnInit() {
        await this.service.init();
        await this.service.auth.allow("/access");
        await this.service.render();
    }

    public isAdmin() {
        return this.service.auth.check.role('admin');
    }

    public async setSourceType(type: 'url' | 'file') {
        this.sourceType = type;
        this.result = null;
        await this.service.render();
    }

    public async selectFile(event: any) {
        const files = event?.target?.files;
        this.selectedFile = files && files.length > 0 ? files[0] : null;
        if (this.selectedFile && !this.paperTitle) {
            this.paperTitle = this.selectedFile.name.replace(/\.[^.]+$/, '');
        }
        this.result = null;
        await this.service.render();
    }

    public async prepareScript() {
        const sourceValue = this.sourceType === 'url'
            ? this.sourceUrl.trim()
            : (this.selectedFile?.name || '');

        if (!sourceValue) {
            await this.service.modal.error(
                this.sourceType === 'url'
                    ? "논문 주소를 입력해주세요."
                    : "논문 파일을 선택해주세요."
            );
            return;
        }

        this.preparing = true;
        this.result = null;
        await this.service.render();

        const { code, data } = await wiz.call("prepare_script", {
            source_type: this.sourceType,
            source_value: sourceValue,
            paper_title: this.paperTitle,
            audience: this.audience,
            duration: this.duration
        });

        this.preparing = false;
        if (code === 200) {
            this.result = data;
        } else {
            await this.service.modal.error(data?.message || data || "대본 초안을 만들지 못했습니다.");
        }
        await this.service.render();
    }

    public openEditor() {
        if (!this.result?.id) return;
        this.service.href(`/posts/${this.result.id}/edit`);
    }
}
