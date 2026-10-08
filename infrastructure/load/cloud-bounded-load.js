// Future bounded cloud smoke load. Run only against an approved pilot URL and token.
// This never generates unbounded traffic and should not be called a sustained SLO test.
import http from 'k6/http';
import { check } from 'k6';

export const options = {
  vus: 2,
  duration: '2m',
  thresholds: {
    http_req_failed: ['rate<0.02'],
    http_req_duration: ['p(95)<2000'],
  },
};

const baseUrl = __ENV.AIOPS_BASE_URL;
const token = __ENV.AIOPS_BEARER_TOKEN;

export default function () {
  if (!baseUrl || !token) {
    throw new Error('AIOPS_BASE_URL and AIOPS_BEARER_TOKEN are required.');
  }
  const response = http.get(`${baseUrl}/api/v1/slo?live_only=true`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  check(response, { 'authenticated SLO API responds': (value) => value.status === 200 });
}
