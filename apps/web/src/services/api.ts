import type { ApiResponse } from "../types/api";

const API_BASE = import.meta.env.VITE_API_BASE ?? "";

export async function fetchApi<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, init);
  if (!response.ok) {
    throw new Error(`API ${response.status}: ${response.statusText}`);
  }
  const payload = (await response.json()) as ApiResponse<T>;
  if (!payload.success) {
    throw new Error(payload.error || payload.message || "API request failed");
  }
  return payload.data;
}
