import { error, redirect } from '@sveltejs/kit';
import { resolve } from '$app/paths';
import { env } from '$env/dynamic/public';

const API_BASE = env.PUBLIC_API_BASE || 'http://localhost:8000';

async function fetchJson(url, fetcher) {
  try {
    const res = await fetcher(url);
    let body = null;
    try {
      body = await res.json();
    } catch {
      body = null;
    }
    return { ok: res.ok, status: res.status, body };
  } catch (err) {
    return {
      ok: false,
      status: 0,
      body: { detail: err?.message ?? 'Network error while contacting API' }
    };
  }
}

function normalizeResponse(body) {
  // Supports both current API shape { recommendations: [book, ...recs] }
  // and potential future shape { book, recommendations }.
  if (body && body.book) {
    const recommendations = Array.isArray(body.recommendations) ? body.recommendations : [];
    return { book: body.book, recommendations };
  }

  const list = Array.isArray(body?.recommendations) ? body.recommendations : [];
  if (list.length === 0) return null;

  return {
    book: list[0],
    recommendations: list.slice(1)
  };
}

export async function load({ params, fetch }) {
  const requestedSlug = params.slug;
  const detailUrl = `${API_BASE}/books/${encodeURIComponent(requestedSlug)}?top_n=10`;
  const direct = await fetchJson(detailUrl, fetch);

  if (direct.ok) {
    const normalized = normalizeResponse(direct.body);
    if (normalized) return normalized;
    throw error(502, 'Book API returned an unexpected payload shape');
  }

  if (direct.status !== 404) {
    throw error(502, `Book API request failed (${direct.status || 'network'})`);
  }

  // Fallback for non-canonical slugs: search by guessed title and redirect.
  const guessedTitle = requestedSlug.replace(/-/g, ' ').trim();
  if (guessedTitle.length > 0) {
    const searchUrl = `${API_BASE}/search?q=${encodeURIComponent(guessedTitle)}&limit=8`;
    const search = await fetchJson(searchUrl, fetch);

    if (!search.ok) {
      throw error(502, `Search API request failed (${search.status || 'network'})`);
    }

    if (Array.isArray(search.body) && search.body.length > 0) {
      const exactMatch = search.body.find((b) => b.slug === requestedSlug);
      const canonicalSlug = exactMatch?.slug ?? search.body[0]?.slug;
      if (canonicalSlug && canonicalSlug !== requestedSlug) {
        throw redirect(307, resolve('/books/[slug]', { slug: canonicalSlug }));
      }
    }
  }

  throw error(404, 'Book not found');
}
