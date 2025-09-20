<script>
  import { onMount } from 'svelte';
  import { fetchBooks, fetchCategories, searchBooks } from '$lib/api.js';
  import { tick } from 'svelte';

  let books = [];
  let page = 1;
  let loading = false;
  const pageSize = 20;
  let error = null;

  // UI state
  let q = '';
  let searching = false;
  let categories = [];
  let activeCategory = '';

  // debounce helper
  let debounceTimer;
  function debounceSearch() {
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
          error = e.message;
        } finally {
          searching = false;
        }
      } else {
        // if query cleared, reload current page
        await loadPage(page);
      }
    }, 450);
  }

  async function loadPage(p = 1) {
    loading = true;
    error = null;
    try {
      const data = await fetchBooks({ page: p, page_size: pageSize });
      books = data;
      page = p;
    } catch (e) {
      console.error(e);
      error = e.message;
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
</style>

<div class="mb-6">
  <div class="flex flex-col sm:flex-row items-start sm:items-center gap-4">
    <div class="flex-1">
      <div class="relative">
        <input
          type="search"
          bind:value={q}
          on:input={debounceSearch}
          placeholder="Search books by title or category..."
          class="w-full rounded-xl border border-gray-200 shadow-sm px-4 py-3 focus:outline-none focus:ring-2 focus:ring-indigo-300"
        />
        <button
          on:click={() => { q=''; loadPage(1); }}
          class="absolute right-2 top-2.5 text-sm text-gray-500 hover:text-gray-800"
          aria-label="clear"
        >✕</button>
      </div>
    </div>

    <div class="flex items-center gap-3">
      <button
        on:click={() => loadPage(Math.max(1, page - 1))}
        class="px-4 py-2 bg-white rounded-lg shadow hover:shadow-md border border-gray-200"
      >
        ← Prev
      </button>
      <div class="text-sm text-gray-600">Page <span class="font-medium">{page}</span></div>
      <button
        on:click={() => loadPage(page + 1)}
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
          class="text-sm px-3 py-1 rounded-full border transition-shadow whitespace-nowrap
                 {activeCategory === c ? 'bg-indigo-600 text-white shadow-md' : 'bg-white text-gray-700 border-gray-200 hover:shadow-sm'}"
          on:click={() => pickCategory(c)}
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
          <a href={`/books/${b.slug}`}>
            <div class="relative rounded-xl overflow-hidden mb-3 h-44 bg-gradient-to-br from-indigo-50 to-white flex items-center justify-center">
              {#if b.img}
                <img src={b.img} alt={b.title} class="object-contain max-h-full w-full" />
              {:else}
                <div class="text-gray-400">No image</div>
              {/if}
              <!-- rating badge -->
              <div class="absolute left-3 top-3 bg-white/90 text-xs px-2 py-1 rounded-full shadow-sm">
                ⭐ {b.rating ?? '-'}
              </div>
              <!-- price pill -->
              <div class="absolute right-3 bottom-3 bg-indigo-600 text-white text-sm px-3 py-1 rounded-full shadow">
                {b.price_clean ? `£${b.price_clean}` : '—'}
              </div>
            </div>
          </a>

          <h3 class="font-semibold text-sm mb-1 line-clamp-2">{b.title}</h3>
          <div class="text-xs text-gray-500 mb-3 capitalize">{b.category}</div>

          <div class="mt-auto flex items-center justify-between gap-2">
            <a href={`/books/${b.slug}`} class="inline-flex items-center px-3 py-2 rounded-lg bg-indigo-600 text-white text-sm hover:bg-indigo-700">
              View
            </a>
            <a href={b.img} target="_blank" rel="noopener" class="text-xs text-gray-500 underline">Cover</a>
          </div>
        </div>
      </article>
    {/each}
  </div>

  <!-- bottom pagination -->
  <div class="flex items-center justify-between mt-8">
    <button on:click={() => loadPage(Math.max(1, page - 1))} class="px-4 py-2 bg-white rounded-lg shadow hover:shadow-md border border-gray-200">Prev</button>
    <div class="text-sm text-gray-600">Showing <span class="font-medium">{books.length}</span> books — Page <span class="font-medium">{page}</span></div>
    <button on:click={() => loadPage(page + 1)} class="px-4 py-2 bg-indigo-600 text-white rounded-lg shadow hover:bg-indigo-700">Next</button>
  </div>
{/if}
