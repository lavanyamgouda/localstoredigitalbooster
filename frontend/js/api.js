const API_BASE = 'http://127.0.0.1:5000/api';

const API = {
  async request(method, endpoint, body = null) {
    const opts = {
      method,
      headers: { 
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
      mode: 'cors',
    };
    if (body) opts.body = JSON.stringify(body);
    try {
      const res = await fetch(`${API_BASE}${endpoint}`, opts);
      const data = await res.json();
      if (!res.ok) throw new Error(data.error || 'Request failed');
      return data;
    } catch (err) {
      console.error(`API ${method} ${endpoint}:`, err.message);
      throw err;
    }
  },
  get:    (ep)       => API.request('GET',    ep),
  post:   (ep, body) => API.request('POST',   ep, body),
  put:    (ep, body) => API.request('PUT',    ep, body),
  delete: (ep)       => API.request('DELETE', ep),
};