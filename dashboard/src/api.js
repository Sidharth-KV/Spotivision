
const API_URL = "http://127.0.0.1:8000";

export async function apiGet(path) {
  const response = await fetch(`${API_URL}${path}`, {
    method: "GET",
    credentials: "include",
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(
      error.detail || `Request failed (${response.status})`
    );
  }

  return response.json();
}
