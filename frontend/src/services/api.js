/**
 * API Service Client for CAREER EXPLORE STUDIO
 * Enhanced in Phase 12 with client-side caching, request deduplication,
 * and unified error formatting for optimal frontend performance.
 */
const API_BASE_URL = '/api';

class ApiService {
  constructor() {
    this.cache = new Map();
    this.inFlight = new Map();
    this.defaultTtlMs = 30000; // 30s cache for idempotent curriculum GET requests
  }

  /**
   * Universal fetch helper with JSON error formatting, request deduplication,
   * and in-memory TTL caching for GET endpoints.
   */
  async request(endpoint, options = {}) {
    const method = (options.method || 'GET').toUpperCase();
    const url = `${API_BASE_URL}${endpoint}`;
    const token =
      options.token ||
      (options.headers && options.headers.Authorization ? options.headers.Authorization.replace(/^Bearer\s+/i, '') : null) ||
      localStorage.getItem('ces_auth_token') ||
      localStorage.getItem('token') ||
      localStorage.getItem('access_token');

    // Cache key incorporates token (for user isolation) and endpoint
    const cacheKey = `${token ? 'auth:' : 'anon:'}${endpoint}`;
    const useCache = method === 'GET' && options.cache !== false;

    // 1. Check valid cache entry for GET requests
    if (useCache && this.cache.has(cacheKey)) {
      const entry = this.cache.get(cacheKey);
      if (Date.now() - entry.timestamp < (options.ttl || this.defaultTtlMs)) {
        return entry.data;
      }
      this.cache.delete(cacheKey);
    }

    // 2. Request deduplication: return existing in-flight request if concurrent
    if (useCache && this.inFlight.has(cacheKey)) {
      return this.inFlight.get(cacheKey);
    }

    const defaultHeaders = {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
    };

    if (token) {
      defaultHeaders['Authorization'] = `Bearer ${token}`;
    }

    const config = {
      ...options,
      headers: {
        ...defaultHeaders,
        ...options.headers,
      },
    };

    const fetchPromise = (async () => {
      try {
        const response = await fetch(url, config);
        const data = await response.json().catch(() => null);

        if (!response.ok) {
          const message = data?.detail || data?.message || 'Something went wrong. Please try again.';
          const error = new Error(typeof message === 'string' ? message : JSON.stringify(message));
          error.status = response.status;
          error.data = data;
          throw error;
        }

        // Cache successful GET results
        if (useCache) {
          this.cache.set(cacheKey, {
            data,
            timestamp: Date.now(),
          });
        }

        // If mutating state (POST/PUT/DELETE), invalidate relevant cache
        if (method !== 'GET') {
          this.invalidateCacheForMutation(endpoint);
        }

        return data;
      } catch (err) {
        if (!err.status) {
          // Network failure or backend unreachable
          err.message = 'Something went wrong. Please check your connection and try again.';
        }
        console.error(`[API Error] ${method} ${url}:`, err.message);
        throw err;
      } finally {
        this.inFlight.delete(cacheKey);
      }
    })();

    if (useCache) {
      this.inFlight.set(cacheKey, fetchPromise);
    }

    return fetchPromise;
  }

  /**
   * Invalidate cache matching specific route patterns upon mutations
   */
  invalidateCacheForMutation(endpoint) {
    if (endpoint.includes('/toggle') || endpoint.includes('/complete') || endpoint.includes('/reset')) {
      this.clearCache('/skills');
      this.clearCache('/progress');
      this.clearCache('/certificates');
    } else if (endpoint.includes('/goals/select')) {
      this.clearCache('/goals');
      this.clearCache('/skills');
      this.clearCache('/progress');
    } else if (endpoint.includes('/evaluation') || endpoint.includes('/overall-evaluation')) {
      this.clearCache('/evaluation');
      this.clearCache('/progress');
      this.clearCache('/certificates');
    } else if (endpoint.includes('/auth/profile')) {
      this.clearCache('/auth/profile');
    } else {
      // Default: clear all cached responses to guarantee freshness
      this.cache.clear();
    }
  }

  /**
   * Clear cache entries matching an optional substring or prefix
   */
  clearCache(pattern = null) {
    if (!pattern) {
      this.cache.clear();
      return;
    }
    for (const key of this.cache.keys()) {
      if (key.includes(pattern)) {
        this.cache.delete(key);
      }
    }
  }

  /**
   * Health check endpoint to verify backend connectivity (no caching)
   */
  async checkHealth() {
    return this.request('/health', { cache: false });
  }
}

export const api = new ApiService();
export default api;
