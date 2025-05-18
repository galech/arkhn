import axios from "axios";

const api = axios.create({
    baseURL: "http://localhost:8000/api",
});

type DeploymentListResponse = {
    deployments: Deployment[];
    cursor: string | null;
};

export class Deployment {
    id: string;
    label: string;
    image: string;
    replicas: number;

    constructor(data?: Partial<Deployment>) {
        this.id = data?.id ?? "";
        this.label = data?.label ?? "";
        this.image = data?.image ?? "";
        this.replicas = data?.replicas ?? 1;
    }

    static async fetch(cursor?: string): Promise<DeploymentListResponse> {
        const response = await api.get(cursor ? cursor : "/deployments/");
        const deployments = response.data.results.map((item: any) => new Deployment(item));
        return {
            deployments,
            cursor: response.data.next,
        };
    }

    async save(): Promise<Deployment> {
        const response = this.id
            ? await api.put(`/deployments/${this.id}/`, this)
            : await api.post("/deployments/", this);
        Object.assign(this, response.data);
    }

    async delete(): Promise<void> {
        await api.delete(`/deployments/${this.id}/`);
    }

}