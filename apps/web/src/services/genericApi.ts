import { fetchApi } from "./api";

export const getStrategyLab = () => fetchApi<any>("/api/strategy/ma-cross");
export const getSignals = () => fetchApi<any>("/api/signal/list");
export const getDataCenter = () => fetchApi<any>("/api/data/status");
export const downloadRealData = () => fetchApi<any>("/api/data/download", { method: "POST" });
export const generateDemoData = () => fetchApi<any>("/api/data/demo", { method: "POST" });
export const getRisk = () => fetchApi<any>("/api/risk/overview");
export const getReports = () => fetchApi<any>("/api/report/list");
export const getSettings = () => fetchApi<any>("/api/settings");
