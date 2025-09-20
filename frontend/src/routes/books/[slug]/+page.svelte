<script context="module">
  import { redirect } from '@sveltejs/kit';
  import { PUBLIC_API_BASE } from '$env/static/public';

  const API_BASE = PUBLIC_API_BASE || 'http://localhost:8000';

  // helper to fetch and parse JSON with details
  async function fetchJson(url, fetcher) {
    const res = await fetcher(url);
    let body = null;
    try { body = await res.json(); } catch (e) { body = null; }
    return { ok: res.ok, status: res.status, body };
  }

  export async function load({ params, fetch }) {
    const slug = params.slug;
    console.log('[load] slug requested:', slug);
    const url = `${API_BASE}/books/${encodeURIComponent(slug)}?top_n=10`;

    // 1) try direct fetch
    try {
      const direct = await fetchJson(url, fetch);
      console.log('[load] direct fetch result:', { url, status: direct.status, ok: direct.ok, bodySample: direct.body ? Object.keys(direct.body).slice(0,5) : null });
      if (direct.ok && direct.body) {
        // sanity check: body.recommendations exists
        if (Array.isArray(direct.body.recommendations) && direct.body.recommendations.length > 0) {
          console.log('[load] direct returned recommendations length=', direct.body.recommendations.length);
          return { data: direct.body };
        } else {
          console.warn('[load] direct returned body but no recommendations array', direct.body);
        }
      } else {
        console.warn('[load] direct fetch not ok', direct.status, direct.body);
      }
    } catch (err) {
      console.error('[load] error during direct fetch', err);
    }

    // 2) fallback: search by guessed title
    const guessedTitle = slug.replace(/-/g, ' ').trim();
    if (guessedTitle) {
      const searchUrl = `${API_BASE}/search?q=${encodeURIComponent(guessedTitle)}&limit=5`;
      try {
        const search = await fetchJson(searchUrl, fetch);
        console.log('[load] search fetch result:', { searchUrl, status: search.status, ok: search.ok, count: Array.isArray(search.body) ? search.body.length : null });
        if (search.ok && Array.isArray(search.body) && search.body.length > 0) {
          const altSlug = search.body[0].slug;
          console.log('[load] search found altSlug:', altSlug);
          // try fetch altSlug
          const altUrl = `${API_BASE}/books/${encodeURIComponent(altSlug)}?top_n=10`;
          const alt = await fetchJson(altUrl, fetch);
          console.log('[load] alt fetch result:', { altUrl, status: alt.status, ok: alt.ok, bodySample: alt.body ? Object.keys(alt.body).slice(0,5) : null });
          if (alt.ok && alt.body && Array.isArray(alt.body.recommendations) && alt.body.recommendations.length > 0) {
            // redirect to canonical slug so URL and data match
            throw redirect(307, `/books/${altSlug}`);
          }
        }
      } catch (err) {
        // allow redirect to bubble up
        if (err?.name === 'Redirect') throw err;
        console.error('[load] error during fallback search', err);
      }
    }

    // nothing found -> 404
    return { status: 404, error: new Error('Book not found') };
  }
</script>

<script>
  // Svelte component script (runes-ready)
  let data = $props();

  // expose raw data for debugging in UI
  let raw = $state(data ?? null);

  // derived view pieces
  let recs = $state(raw?.recommendations ?? []);
  let detail = $state(recs.length ? recs[0] : null);

  // safe format
  function formatPrice(p) { return p == null ? '-' : `£${p}`; }
</script>

<style>
  .card-title { display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
</style>

<!-- Debug banner -->
<div class="p-3 bg-yellow-50 border-l-4 border-yellow-400 mb-4">
  <strong>Debug:</strong> This page shows raw `data` for debugging. Remove debug UI after fix.
</div>

<pre class="bg-gray-900 text-white p-3 rounded mb-4 overflow-auto" style="max-height:200px;">
{JSON.stringify(raw, null, 2)}
</pre>

{#if !detail}
  <div class="p-8 text-center">
    <h2 class="text-xl font-semibold mb-2">Book not found</h2>
    <p class="text-sm text-gray-600">We couldn't find that book. Use the debug output above.</p>
    <a href="/" class="inline-block mt-4 px-4 py-2 bg-indigo-600 text-white rounded">Back to home</a>
  </div>
{:else}
  <div class="grid md:grid-cols-3 gap-6">
    <div class="md:col-span-1 bg-white p-4 rounded shadow">
      {#if detail.img}
        <img src={detail.img} alt={detail.title} class="w-full mb-4" loading="lazy" decoding="async" />
      {/if}
      <h2 class="text-xl font-semibold">{detail.title}</h2>
      <div class="text-sm text-gray-500 mb-2">{detail.category}</div>
      <div class="mb-2">⭐ {detail.rating ?? '-'}</div>
      <div class="font-bold mb-4">{formatPrice(detail.price_clean)}</div>
      <div class="text-sm text-gray-700 whitespace-pre-line">{detail.description}</div>
    </div>

    <div class="md:col-span-2">
      <h3 class="text-lg font-semibold mb-4">Recommended from the same category</h3>
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
        {#each recs.slice(1) as r}
          <a href={`/books/${r.slug}`} sveltekit:prefetch class="bg-white p-3 rounded shadow hover:shadow-md flex">
            <div class="w-20 h-28 bg-gray-100 mr-3 flex items-center justify-center overflow-hidden">
              {#if r.img}
                <img src={r.img} alt={r.title} class="max-h-full" loading="lazy" decoding="async" />
              {:else}
                <div class="text-gray-400">No image</div>
              {/if}
            </div>
            <div class="flex-1">
              <div class="font-medium">{r.title}</div>
              <div class="text-xs text-gray-500">⭐ {r.rating ?? '-'}</div>
              <div class="text-sm mt-2">{formatPrice(r.price_clean)}</div>
            </div>
          </a>
        {/each}
      </div>
    </div>
  </div>
{/if}
