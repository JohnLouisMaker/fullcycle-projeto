import { check, sleep } from "k6";
import http from "k6/http";

const API_URL = (__ENV.API_URL || "http://localhost:8000").replace(/\/$/, "");

export const options = {
  vus: 5,
  duration: "30s",
  summaryTrendStats: ["avg", "min", "med", "max", "p(90)", "p(95)", "p(99)"],
  thresholds: {
    http_req_duration: ["p(95)<200"],
    http_req_failed: ["rate<0.01"],
    checks: ["rate>0.99"],
  },
};

export default function () {
  const response = http.get(`${API_URL}/livros`, {
    tags: { endpoint: "GET /livros" },
  });

  check(response, {
    "GET /livros retorna HTTP 200": (res) => res.status === 200,
    "tempo individual de resposta < 200 ms": (res) =>
      res.timings.duration < 200,
  });

  sleep(1);
}
