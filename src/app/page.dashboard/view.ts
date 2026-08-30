import { OnInit } from '@angular/core';
import { Service } from '@wiz/libs/portal/season/service';

export class Component implements OnInit {
    public stats: any[] = [];
    public recentItems: any[] = [];
    public loading: boolean = true;

    constructor(public service: Service) { }

    public async ngOnInit() {
        await this.service.init();
        await this.service.auth.allow("/access");
        await this.load();
    }

    public async load() {
        this.loading = true;
        await this.service.render();

        try {
            const { code, data } = await wiz.call("overview");
            if (code !== 200) {
                throw new Error("대시보드 API 응답 오류");
            }

            this.stats = (data && data.stats) || [];
            this.recentItems = (data && data.recent) || [];
        } catch (error) {
            this.stats = [];
            this.recentItems = [];
            console.error("대시보드 조회 실패", error);
        } finally {
            this.loading = false;
            await this.service.render();
        }
    }
}
