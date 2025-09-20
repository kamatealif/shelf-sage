<script>
  import { onMount, onDestroy } from 'svelte';
  import { fetchBooks, fetchCategories, searchBooks } from '$lib/api.js';
  import { tick } from 'svelte';

  // ---------- Svelte 5 runes (reactive state) ----------
  // use $state(...) for reactive top-level state
  let books = $state([]);         // array of book summaries
  let page = $state(1);          
  let loading = $state(false);
  const pageSize = 20;           // constant, not reactive
  let error = $state(null);

  // UI state
  let q = $state('');
  let searching = $state(false);
  let categories = $state([]);
  let activeCategory = $state('');

  // non-reactive timer handle
  let debounceTimer;

  // ---------- helpers ----------
  function setError(e) {
    // support Error objects thrown by our improved api helper (may have .body)
    error = e?.body?.detail || e?.message || String(e);
  }

  async function debounceSearch() {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(async () => {
      if (q && q.length > 0) {
        searching = true;
        try {
          const res = await searchBooks(q);
          books = res;
          page = 1;
        } catch (e) {
          console.error(e);
          setError(e);
        } finally {
          searching = false;
        }
      } else {
        // if query cleared, reload current page
        await loadPage(page);
      }
    }, 450);
  }

  // ensure timer cleared when component unmounts
  onDestroy(() => {
    clearTimeout(debounceTimer);
  });

  async function loadPage(p = 1) {
    loading = true;
    error = null;
    try {
      const data = await fetchBooks({ page: p, page_size: pageSize });
      books = data;
      page = p;
    } catch (e) {
      console.error(e);
      setError(e);
    } finally {
      loading = false;
    }
    await tick();
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  async function loadCategories() {
    try {
      categories = await fetchCategories();
    } catch (e) {
      console.error('Failed to load categories', e);
    }
  }

  function pickCategory(cat) {
    activeCategory = cat;
    q = cat;
    debounceSearch();
  }

  onMount(() => {
    loadCategories();
    loadPage(1);
  });
</script>

<style>
  /* small custom tweaks on top of Tailwind */
  .glass {
    background: linear-gradient(180deg, rgba(255,255,255,0.75), rgba(255,255,255,0.6));
    backdrop-filter: blur(6px);
  }

  /* fallback two-line clamp for card titles (works even without Tailwind plugin) */
  .card-title {
    display: -webkit-box;
    -webkit-box-orient: vertical;
    -webkit-line-clamp: 2;
    overflow: hidden;
    text-overflow: ellipsis;
  }
</style>

<!-- UI -->
<div class="mb-6">
  <div class="flex flex-col sm:flex-row items-start sm:items-center gap-4">
    <div class="flex-1">
      <div class="relative">
        <!-- Svelte 5 event attributes: use `oninput` / `onclick` -->
        <input
          type="search"
          bind:value={q}
          oninput={debounceSearch}
          placeholder="Search books by title or category..."
          class="w-full rounded-xl border border-gray-200 shadow-sm px-4 py-3 focus:outline-none focus:ring-2 focus:ring-indigo-300"
        />
        <button
          type="button"
          onclick={() => { q=''; loadPage(1); }}
          class="absolute right-2 top-2.5 text-sm text-gray-500 hover:text-gray-800"
          aria-label="clear"
        >✕</button>
      </div>
    </div>

    <div class="flex items-center gap-3">
      <button
        type="button"
        onclick={() => loadPage(Math.max(1, page - 1))}
        class="px-4 py-2 bg-white rounded-lg shadow hover:shadow-md border border-gray-200"
      >
        ← Prev
      </button>
      <div class="text-sm text-gray-600">Page <span class="font-medium">{page}</span></div>
      <button
        type="button"
        onclick={() => loadPage(page + 1)}
        class="px-4 py-2 bg-indigo-600 text-white rounded-lg shadow hover:bg-indigo-700"
      >
        Next →
      </button>
    </div>
  </div>

  <!-- Category chips -->
  <div class="mt-4 overflow-x-auto py-2">
    <div class="flex gap-2">
      {#each categories.slice(0, 12) as c}
        <button
          type="button"
          class="text-sm px-3 py-1 rounded-full border transition-shadow whitespace-nowrap
                 {activeCategory === c ? 'bg-indigo-600 text-white shadow-md' : 'bg-white text-gray-700 border-gray-200 hover:shadow-sm'}"
          onclick={() => pickCategory(c)}
        >
          {c}
        </button>
      {/each}
      {#if categories.length === 0}
        <div class="text-sm text-gray-400">No categories loaded</div>
      {/if}
    </div>
  </div>
</div>

{#if loading || searching}
  <!-- skeleton grid -->
  <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
    {#each Array(12) as _}
      <div class="animate-pulse bg-white rounded-xl p-4">
        <div class="h-40 bg-gray-200 rounded-md mb-4"></div>
        <div class="h-4 bg-gray-200 rounded w-3/4 mb-2"></div>
        <div class="h-3 bg-gray-200 rounded w-1/2 mb-4"></div>
        <div class="flex justify-between items-center">
          <div class="h-6 w-20 bg-gray-200 rounded"></div>
          <div class="h-6 w-10 bg-gray-200 rounded"></div>
        </div>
      </div>
    {/each}
  </div>
{:else if error}
  <div class="text-red-600">Error: {error}</div>
{:else}
  <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
    {#each books as b}
      <article class="glass rounded-2xl p-4 shadow-sm hover:shadow-lg transform hover:-translate-y-1 transition-all duration-200">
        <div class="flex flex-col h-full">
          <!-- internal link prefetch for snappy navigation -->
          <a href={`/books/${b.slug}`} sveltekit:prefetch class="block" aria-label={`Open ${b.title}`}>
            <div class="relative rounded-xl overflow-hidden mb-3 h-44 bg-gradient-to-br from-indigo-50 to-white flex items-center justify-center">
              {#if b.img}
                <img src={b.img} alt={b.title} loading="lazy" decoding="async" class="object-contain max-h-full w-full" />
              {:else}
                <div class="text-gray-400">No image</div>
              {/if}
              <div class="absolute left-3 top-3 bg-white/90 text-xs px-2 py-1 rounded-full shadow-sm">
                ⭐ {b.rating ?? '-'}
              </div>
              <div class="absolute right-3 bottom-3 bg-indigo-600 text-white text-sm px-3 py-1 rounded-full shadow">
                {b.price_clean ? `£${b.price_clean}` : '—'}
              </div>
            </div>

            <h3 class="font-semibold text-sm mb-1 card-title">{b.title}</h3>
            <div class="text-xs text-gray-500 mb-3 capitalize">{b.category}</div>
          </a>

          <div class="mt-auto flex items-center justify-between gap-2">
            <button
              type="button"
              onclick={() => (location.href = `/books/${b.slug}`)}
              class="inline-flex items-center px-3 py-2 rounded-lg bg-indigo-600 text-white text-sm hover:bg-indigo-700"
              aria-label={`View ${b.title}`}
            >
              View
            </button>
            {#if b.img}
              <a href={b.img} target="_blank" rel="noopener noreferrer" class="text-xs text-gray-500 underline">Cover</a>
            {/if}
          </div>
        </div>
      </article>
    {/each}
  </div>

  <!-- bottom pagination -->
  <div class="flex items-center justify-between mt-8">
    <button type="button" onclick={() => loadPage(Math.max(1, page - 1))} class="px-4 py-2 bg-white rounded-lg shadow hover:shadow-md border border-gray-200">Prev</button>
    <div class="text-sm text-gray-600">Showing <span class="font-medium">{books.length}</span> books — Page <span class="font-medium">{page}</span></div>
    <button type="button" onclick={() => loadPage(page + 1)} class="px-4 py-2 bg-indigo-600 text-white rounded-lg shadow hover:bg-indigo-700">Next</button>
  </div>
{/if}
