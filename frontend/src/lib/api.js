// src/lib/api.js
import { PUBLIC_API_BASE } from '$env/static/public';

const API_BASE = PUBLIC_API_BASE || 'http://localhost:8000';

export async function fetchBooks({ page = 1, page_size = 20, fetcher = fetch } = {}) {
	const url = `${API_BASE}/?page=${page}&page_size=${page_size}`;
	const res = await fetcher(url);
	if (!res.ok) throw new Error('Failed to fetch books');
	return res.json();
}

export async function fetchBookBySlug(slug, top_n = 10, fetcher = fetch) {
	const url = `${API_BASE}/books/${encodeURIComponent(slug)}?top_n=${top_n}`;
	const res = await fetcher(url);
	if (!res.ok) throw new Error('Failed to fetch book');
	return res.json();
}

export async function fetchCategories(fetcher = fetch) {
	const url = `${API_BASE}/categories`;
	const res = await fetcher(url);
	if (!res.ok) throw new Error('Failed to fetch categories');
	return res.json();
}

export async function searchBooks(q, limit = 20, fetcher = fetch) {
	const url = `${API_BASE}/search?q=${encodeURIComponent(q)}&limit=${limit}`;
	const res = await fetcher(url);
	if (!res.ok) throw new Error('Search failed');
	return res.json();
}
