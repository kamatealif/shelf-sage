<script>
  import { onMount, onDestroy, tick } from 'svelte';
  import { fetchBooks, fetchCategories, searchBooks } from '$lib/api.js';

  let books = $state([]);
  let page = $state(1);
  let loading = $state(false);
  let error = $state(null);
  const pageSize = 20;

  let q = $state('');
  let searching = $state(false);
  let categories = $state([]);
  let activeCategory = $state('');

  let debounceTimer;

  function setError(e) {
    error = e?.body?.detail || e?.message || String(e);
  }

  function formatPrice(price) {
    if (price === null || price === undefined || Number.isNaN(Number(price))) return 'Price N/A';
    return `£${Number(price).toFixed(2)}`;
  }

  async function debounceSearch() {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(async () => {
      if (q && q.length > 0) {
        searching = true;
        error = null;
        try {
          books = await searchBooks(q);
          page = 1;
        } catch (e) {
          setError(e);
        } finally {
          searching = false;
        }
      } else {
        await loadPage(page);
      }
    }, 360);
  }

  function onSearchInput() {
    activeCategory = '';
    debounceSearch();
  }

  function pickCategory(cat) {
    activeCategory = cat;
    q = cat;
    debounceSearch();
  }

  function clearSearch() {
    q = '';
    activeCategory = '';
    loadPage(1);
  }

  onDestroy(() => {
    clearTimeout(debounceTimer);
  });

  async function loadPage(p = 1) {
    loading = true;
    error = null;
    try {
      books = await fetchBooks({ page: p, page_size: pageSize });
      page = p;
    } catch (e) {
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

  onMount(() => {
    loadCategories();
    loadPage(1);
  });
</script>

<style>
  .hero-surface {
    background:
      linear-gradient(135deg, rgba(255, 255, 255, 0.85), rgba(240, 253, 250, 0.65)),
      linear-gradient(0deg, rgba(255, 255, 255, 0.5), rgba(255, 255, 255, 0.5));
    border: 1px solid var(--stroke);
    box-shadow: 0 22px 40px rgba(15, 23, 42, 0.08);
  }

  .control-surface {
    background: var(--surface);
    border: 1px solid var(--stroke);
    box-shadow: 0 14px 30px rgba(15, 23, 42, 0.06);
  }

  .book-card {
    position: relative;
    overflow: hidden;
    border-radius: 1.25rem;
    border: 1px solid var(--stroke);
    background: var(--surface-strong);
    box-shadow: 0 10px 28px rgba(15, 23, 42, 0.08);
    transition: transform 0.25s ease, box-shadow 0.25s ease;
  }

  .book-card::after {
    content: '';
    position: absolute;
    inset: 0;
    pointer-events: none;
    background: linear-gradient(145deg, rgba(13, 148, 136, 0.14), transparent 45%);
    opacity: 0;
    transition: opacity 0.25s ease;
  }

  .book-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 18px 36px rgba(15, 23, 42, 0.12);
  }

  .book-card:hover::after {
    opacity: 1;
  }

  .book-cover-wrap {
    aspect-ratio: 4 / 5;
    background: linear-gradient(160deg, rgba(204, 251, 241, 0.75), rgba(255, 237, 213, 0.55));
  }

  .book-cover {
    transition: transform 0.32s ease;
  }

  .book-card:hover .book-cover {
    transform: scale(1.06);
  }

  .card-title {
    display: -webkit-box;
    overflow: hidden;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
  }

  .chip-scroll {
    scrollbar-width: thin;
    scrollbar-color: rgba(15, 118, 110, 0.32) transparent;
  }

  .chip-scroll::-webkit-scrollbar {
    height: 6px;
  }

  .chip-scroll::-webkit-scrollbar-thumb {
    border-radius: 999px;
    background: rgba(15, 118, 110, 0.32);
  }
</style>

<section class="hero-surface mb-6 rounded-3xl p-6 sm:p-8">
  <div class="grid gap-6 lg:grid-cols-[1.25fr_0.75fr]">
    <div>
      <p class="mb-3 text-xs font-semibold uppercase tracking-[0.2em] text-teal-700">Modern Book Discovery</p>
      <h1 class="text-3xl font-extrabold text-slate-900 sm:text-4xl">Find the right book in seconds</h1>
      <p class="mt-3 max-w-2xl text-sm text-slate-600 sm:text-base">
        Search by title, jump by category, and explore curated recommendations from a clean dataset of one thousand books.
      </p>
      <div class="mt-5 flex flex-wrap gap-2 text-xs sm:text-sm">
        <span class="rounded-full border border-teal-200 bg-teal-50 px-3 py-1 font-semibold text-teal-800">Showing {books.length} books</span>
        <span class="rounded-full border border-slate-200 bg-white px-3 py-1 font-semibold text-slate-700">Page {page}</span>
        <span class="rounded-full border border-orange-200 bg-orange-50 px-3 py-1 font-semibold text-orange-700">{categories.length} categories</span>
      </div>
    </div>
    <div class="rounded-2xl border border-white/70 bg-white/75 p-4 shadow-sm">
      <h2 class="text-sm font-bold uppercase tracking-[0.16em] text-slate-500">Quick Tips</h2>
      <ul class="mt-3 space-y-2 text-sm text-slate-600">
        <li>Use category chips for instant focused browsing.</li>
        <li>Type any keyword to search title and category together.</li>
        <li>Open a card to get related recommendations.</li>
      </ul>
    </div>
  </div>
</section>

<section class="control-surface mb-6 rounded-3xl p-4 sm:p-6">
  <div class="flex flex-col gap-4 lg:flex-row lg:items-center">
    <div class="relative flex-1">
      <span class="pointer-events-none absolute left-3 top-3 text-slate-400">⌕</span>
      <input
        type="search"
        bind:value={q}
        oninput={onSearchInput}
        placeholder="Search by title or category..."
        class="w-full rounded-2xl border-slate-200 bg-white/85 py-3 pl-10 pr-14 text-sm text-slate-800 placeholder:text-slate-400 focus:border-teal-400 focus:ring-2 focus:ring-teal-200"
      />
      {#if q}
        <button
          type="button"
          onclick={clearSearch}
          class="absolute right-2 top-2 rounded-xl border border-slate-200 px-3 py-1 text-xs font-semibold text-slate-600 hover:border-slate-300 hover:bg-slate-50"
          aria-label="Clear search"
        >
          Clear
        </button>
      {/if}
    </div>
    <div class="flex w-full gap-2 sm:w-auto">
      <button
        type="button"
        onclick={() => loadPage(Math.max(1, page - 1))}
        disabled={page <= 1 || searching || q.trim().length > 0}
        class={`flex-1 rounded-xl border px-4 py-2 text-sm font-semibold transition sm:flex-none ${
          page <= 1 || searching || q.trim().length > 0
            ? 'cursor-not-allowed border-slate-200 bg-slate-100 text-slate-400'
            : 'border-slate-200 bg-white text-slate-700 hover:-translate-y-0.5 hover:border-teal-300 hover:text-teal-800'
        }`}
      >
        Previous
      </button>
      <button
        type="button"
        onclick={() => loadPage(page + 1)}
        disabled={searching || q.trim().length > 0}
        class={`flex-1 rounded-xl border px-4 py-2 text-sm font-semibold transition sm:flex-none ${
          searching || q.trim().length > 0
            ? 'cursor-not-allowed border-teal-300 bg-teal-200/70 text-teal-700'
            : 'border-teal-700 bg-teal-700 text-white hover:-translate-y-0.5 hover:bg-teal-800'
        }`}
      >
        Next
      </button>
    </div>
  </div>

  <div class="chip-scroll mt-4 overflow-x-auto pb-1">
    <div class="flex w-max gap-2 pr-2">
      <button
        type="button"
        onclick={clearSearch}
        class={`rounded-full border px-3 py-1.5 text-xs font-semibold uppercase tracking-wide transition ${
          activeCategory === '' && q === ''
            ? 'border-teal-700 bg-teal-700 text-white'
            : 'border-slate-200 bg-white text-slate-700 hover:border-teal-300 hover:text-teal-800'
        }`}
      >
        All
      </button>
      {#each categories as c}
        <button
          type="button"
          onclick={() => pickCategory(c)}
          class={`rounded-full border px-3 py-1.5 text-xs font-semibold capitalize transition ${
            activeCategory === c
              ? 'border-teal-700 bg-teal-700 text-white'
              : 'border-slate-200 bg-white text-slate-700 hover:border-teal-300 hover:text-teal-800'
          }`}
        >
          {c}
        </button>
      {/each}
      {#if categories.length === 0}
        <div class="rounded-full border border-slate-200 bg-white px-3 py-1.5 text-xs text-slate-500">Loading categories...</div>
      {/if}
    </div>
  </div>
</section>

{#if loading || searching}
  <div class="grid gap-5 sm:grid-cols-2 xl:grid-cols-3 2xl:grid-cols-4">
    {#each Array(8) as _}
      <article class="animate-pulse rounded-3xl border border-white/70 bg-white/70 p-4 shadow-sm">
        <div class="mb-3 h-48 rounded-2xl bg-slate-200/80"></div>
        <div class="mb-2 h-4 w-3/4 rounded bg-slate-200/80"></div>
        <div class="mb-4 h-4 w-1/2 rounded bg-slate-200/80"></div>
        <div class="flex items-center justify-between">
          <div class="h-6 w-20 rounded-full bg-slate-200/80"></div>
          <div class="h-6 w-14 rounded-full bg-slate-200/80"></div>
        </div>
      </article>
    {/each}
  </div>
{:else if error}
  <div class="rounded-2xl border border-red-200 bg-red-50 p-5 text-sm text-red-700">
    <span class="font-semibold">Request failed:</span> {error}
  </div>
{:else if books.length === 0}
  <div class="rounded-2xl border border-slate-200 bg-white/80 p-8 text-center shadow-sm">
    <h2 class="text-xl font-bold text-slate-900">No books found</h2>
    <p class="mt-2 text-sm text-slate-600">Try another search keyword or reset your category filters.</p>
    <button
      type="button"
      onclick={clearSearch}
      class="mt-4 rounded-xl border border-teal-700 bg-teal-700 px-4 py-2 text-sm font-semibold text-white hover:bg-teal-800"
    >
      Reset Filters
    </button>
  </div>
{:else}
  <div class="grid gap-5 sm:grid-cols-2 xl:grid-cols-3 2xl:grid-cols-4">
    {#each books as b}
      <article class="book-card">
        <a href={`/books/${b.slug}`} data-sveltekit-preload-data="hover" class="flex h-full flex-col">
          <div class="book-cover-wrap relative m-3 overflow-hidden rounded-2xl">
            {#if b.img}
              <img src={b.img} alt={b.title} loading="lazy" decoding="async" class="book-cover h-full w-full object-contain p-3" />
            {:else}
              <div class="grid h-full place-items-center text-sm font-medium text-slate-500">No cover available</div>
            {/if}
            <div class="absolute left-2 top-2 rounded-full bg-white/90 px-2 py-1 text-xs font-semibold text-slate-700 shadow-sm">
              ⭐ {b.rating ?? '-'}
            </div>
          </div>

          <div class="flex flex-1 flex-col px-4 pb-4">
            <div class="mb-3 flex items-center justify-between gap-2 text-xs">
              <span class="truncate rounded-full bg-teal-50 px-3 py-1 font-semibold capitalize text-teal-700">{b.category}</span>
              <span class="shrink-0 text-sm font-extrabold text-slate-900">{formatPrice(b.price_clean)}</span>
            </div>

            <h3 class="card-title mb-4 text-base font-bold leading-snug text-slate-900">{b.title}</h3>

            <div class="mt-auto flex items-center justify-between gap-2">
              <span class="text-xs font-medium text-slate-500">
                {b.rating !== null && b.rating !== undefined ? `Rating ${b.rating}/5` : 'Unrated'}
              </span>
              <span class="rounded-full bg-slate-900 px-3 py-1 text-xs font-semibold text-white">Details</span>
            </div>
          </div>
        </a>
      </article>
    {/each}
  </div>

  <div class="mt-8 flex flex-col gap-4 rounded-2xl border border-white/70 bg-white/75 p-4 shadow-sm sm:flex-row sm:items-center sm:justify-between">
    <div class="text-sm text-slate-600">
      Showing <span class="font-bold text-slate-900">{books.length}</span> books on page
      <span class="font-bold text-slate-900">{page}</span>
    </div>
    <div class="flex gap-2">
      <button
        type="button"
        onclick={() => loadPage(Math.max(1, page - 1))}
        disabled={page <= 1 || searching || q.trim().length > 0}
        class={`rounded-xl border px-4 py-2 text-sm font-semibold transition ${
          page <= 1 || searching || q.trim().length > 0
            ? 'cursor-not-allowed border-slate-200 bg-slate-100 text-slate-400'
            : 'border-slate-200 bg-white text-slate-700 hover:border-teal-300 hover:text-teal-800'
        }`}
      >
        Previous
      </button>
      <button
        type="button"
        onclick={() => loadPage(page + 1)}
        disabled={searching || q.trim().length > 0}
        class={`rounded-xl border px-4 py-2 text-sm font-semibold transition ${
          searching || q.trim().length > 0
            ? 'cursor-not-allowed border-teal-300 bg-teal-200/70 text-teal-700'
            : 'border-teal-700 bg-teal-700 text-white hover:bg-teal-800'
        }`}
      >
        Next
      </button>
    </div>
  </div>
{/if}
