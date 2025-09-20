<script context="module">
  import { fetchBookBySlug, searchBooks } from '$lib/api.js';

  /**
   * Robust load: try direct slug -> if 404 try fallback search by title guess (hyphens -> spaces)
   * Returns { props: { data } } on success
   * Returns { status: 404, error: new Error('Book not found') } on failure
   */
  export async function load({ params, fetch }) {
    const slug = params.slug;
    // quick sanity
    console.debug('[load] book slug:', slug);

    // 1) Try direct fetch by slug
    try {
      const data = await fetchBookBySlug(slug, 10, fetch); // note: our api helper accepts fetcher
      // ensure structure
      if (data && data.recommendations && data.recommendations.length > 0) {
        return { props: { data } };
      }
      // if API returned something unexpected, fallthrough to fallback
      console.warn('[load] fetchBookBySlug returned no recommendations, falling back', data);
    } catch (err) {
      console.warn('[load] fetchBookBySlug failed for slug:', slug, err);
      // fallthrough to fallback attempt
    }

    // 2) Fallback: guess title from slug (replace hyphens) and call search endpoint
    const guessedTitle = slug.replace(/-/g, ' ').trim();
    if (guessedTitle.length > 0) {
      try {
        const searchRes = await searchBooks(guessedTitle, 5, fetch); // returns array of book summaries
        console.debug('[load] search results for guessedTitle:', guessedTitle, searchRes?.length);
        if (Array.isArray(searchRes) && searchRes.length > 0) {
          // pick the first match and try fetch by its slug
          const altSlug = searchRes[0].slug;
          try {
            const altData = await fetchBookBySlug(altSlug, 10, fetch);
            if (altData && altData.recommendations && altData.recommendations.length > 0) {
              // Redirect to canonical slug (optional) OR return altData so page renders
              return {
                // Option A: return altData and keep URL as-is
                props: { data: altData },
                // Option B (recommended): redirect to canonical slug so URL matches API
                // redirect: `/books/${altSlug}`
              };
            }
          } catch (err2) {
            console.warn('[load] fetchBookBySlug failed for altSlug:', altSlug, err2);
          }
        }
      } catch (err) {
        console.warn('[load] searchBooks failed for guessedTitle:', guessedTitle, err);
      }
    }

    // 3) Give up — return 404 to SvelteKit
    return { status: 404, error: new Error('Book not found') };
  }
</script>


<script>
    export let data;
  // data: { recommendations: [ { slug, title, img, category, rating,
  const recs = data.recommendations || [];
  const detail = recs[0] || null;
</script>

{#if !detail}
  <div>Book not found</div>
{:else}
  <div class="grid md:grid-cols-3 gap-6">
    <div class="md:col-span-1 bg-white p-4 rounded shadow">
      {#if detail.img}
        <img src={detail.img} alt={detail.title} class="w-full mb-4" />
      {/if}
      <h2 class="text-xl font-semibold">{detail.title}</h2>
      <div class="text-sm text-gray-500 mb-2">{detail.category}</div>
      <div class="mb-2">⭐ {detail.rating ?? '-'}</div>
      <div class="font-bold mb-4">{detail.price_clean ? `£${detail.price_clean}` : '-'}</div>
      <div class="text-sm text-gray-700 whitespace-pre-line">{detail.description}</div>
    </div>

    <div class="md:col-span-2">
      <h3 class="text-lg font-semibold mb-4">Recommended from the same category</h3>
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
        {#each recs.slice(1) as r}
          <a href={`/books/${r.slug}`} class="bg-white p-3 rounded shadow hover:shadow-md flex">
            <div class="w-20 h-28 bg-gray-100 mr-3 flex items-center justify-center overflow-hidden">
              {#if r.img}
                <img src={r.img} alt={r.title} class="max-h-full"/>
              {:else}
                <div class="text-gray-400">No image</div>
              {/if}
            </div>
            <div class="flex-1">
              <div class="font-medium">{r.title}</div>
              <div class="text-xs text-gray-500">⭐ {r.rating ?? '-'}</div>
              <div class="text-sm mt-2">{r.price_clean ? `£${r.price_clean}` : '-'}</div>
            </div>
          </a>
        {/each}
      </div>
    </div>
  </div>
{/if}
