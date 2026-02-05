import { BACKEND_API_ENDPOINT } from "@/constants";
import type { APIResponse } from "@/types";

export async function makePrediction(input: string): Promise<APIResponse> {
  const response = await fetch(BACKEND_API_ENDPOINT, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text: input }),
  });

  const result = await response.json();
  
  return result;
}
