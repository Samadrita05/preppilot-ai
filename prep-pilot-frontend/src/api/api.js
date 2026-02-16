const API_URL = "https://preppilot-backend.onrender.com";

export const api = async (endpoint, options = {}) => {
  const token = localStorage.getItem("token");

  const res = await fetch(`${API_URL}${endpoint}`, {
    method: options.method || "GET",
    headers: {
      "Content-Type": "application/json",
      Authorization: token ? `Bearer ${token}` : "",
    },
    body: options.body ? JSON.stringify(options.body) : null,
  });

  if (!res.ok) {
    let err;
    try {
      err = await res.json();
    } catch {
      throw new Error("Request failed");
    }
    throw new Error(err.detail || "Request failed");
  }

  return res.json();
};
