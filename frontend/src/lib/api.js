// src/lib/api.js
import { env } from '$env/dynamic/public';

const API_BASE = env.PUBLIC_API_BASE || 'http://localhost:8000';

async function parseJsonSafe(res) {
	try {
		return await res.json();
	} catch (err) {
		return null;
	}
}

async function fetchWithDetails(url, fetcher = fetch) {
	const res = await fetcher(url);
	const body = await parseJsonSafe(res);
	if (!res.ok) {
		const msg = body && body.detail ? body.detail : body || `HTTP ${res.status}`;
		const err = new Error(`Request failed: ${msg}`);
		err.status = res.status;
		err.body = body;
		throw err;
	}
	return body;
}

export async function fetchBooks({ page = 1, page_size = 20, fetcher = fetch } = {}) {
	const url = `${API_BASE}/?page=${page}&page_size=${page_size}`;
	return fetchWithDetails(url, fetcher);
}

export async function fetchBookBySlug(slug, top_n = 10, fetcher = fetch) {
	const url = `${API_BASE}/books/${encodeURIComponent(slug)}?top_n=${top_n}`;
	return fetchWithDetails(url, fetcher);
}

export async function fetchCategories(fetcher = fetch) {
	const url = `${API_BASE}/categories`;
	return fetchWithDetails(url, fetcher);
}

export async function searchBooks(q, limit = 20, fetcher = fetch) {
	const url = `${API_BASE}/search?q=${encodeURIComponent(q)}&limit=${limit}`;
	return fetchWithDetails(url, fetcher);
}

export default { fetchBooks, fetchBookBySlug, fetchCategories, searchBooks };
