import { fetchApi } from "./api";
import type { DashboardOverview } from "../types/api";

export const getDashboardOverview = () => fetchApi<DashboardOverview>("/api/dashboard/overview");
