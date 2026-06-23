import { fetchApi } from "./api";
import type { PortfolioData } from "../types/api";

export const getPortfolioOverview = () => fetchApi<PortfolioData>("/api/portfolio/overview");
