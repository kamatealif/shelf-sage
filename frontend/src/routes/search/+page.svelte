<script>
  import { onMount } from 'svelte';
  import { get } from 'svelte/store';
  import { resolve } from '$app/paths';
  import { page } from '$app/stores';
  import { fetchCategories, searchBooks } from '$lib/api';

  let q = '';
  let results = [];
  let loading = false;
  let error = null;
  let categories = [];
  const skeletonRows = Array.from({ length: 8 }, (_, i) => i);

  onMount(async () => {
    const qp = get(page).url.searchParams.get('q') || '';
    q = qp;

    try {
      categories = (await fetchCategories()).slice(0, 10);
    } catch {
      categories = [];
    }

    if (qp) {
      await doSearch(qp);
    }
  });

  async function doSearch(query) {
    const term = String(query || '').trim();
    if (!term) {
      results = [];
      error = null;
      return;
    }

    loading = true;
    error = null;
    try {
      results = await searchBooks(term, 60);
    } catch (e) {
      console.error(e);
      results = [];
      error = e?.body?.detail || e?.message || 'Search failed';
    } finally {
      loading = false;
    }
  }

  function clearSearch() {
    q = '';
    results = [];
    error = null;
  }

  function pickQuick(term) {
    q = term;
    doSearch(term);
  }

  function formatPrice(price) {
    if (price === null || price === undefined || Number.isNaN(Number(price))) return 'Price N/A';
    return `£${Number(price).toFixed(2)}`;
  }
</script>

<style>
  .hero-surface {
    background:
      linear-gradient(140deg, rgba(255, 255, 255, 0.88), rgba(240, 253, 250, 0.7)),
      linear-gradient(0deg, rgba(255, 255, 255, 0.5), rgba(255, 255, 255, 0.5));
    border: 1px solid var(--stroke);
    box-shadow: 0 22px 40px rgba(15, 23, 42, 0.08);
  }

  .panel-surface {
    background: var(--surface);
    border: 1px solid var(--stroke);
    box-shadow: 0 14px 30px rgba(15, 23, 42, 0.06);
  }

  .book-card {
    border: 1px solid var(--stroke);
    background: var(--surface-strong);
    box-shadow: 0 10px 26px rgba(15, 23, 42, 0.08);
    transition: transform 0.24s ease, box-shadow 0.24s ease;
  }

  .book-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 18px 34px rgba(15, 23, 42, 0.12);
  }

  .book-cover-wrap {
    aspect-ratio: 4 / 5;
    background: linear-gradient(160deg, rgba(204, 251, 241, 0.75), rgba(255, 237, 213, 0.55));
  }

  .title-clamp {
    display: -webkit-box;
    overflow: hidden;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
  }
</style>

<section class="hero-surface mb-6 rounded-3xl p-6 sm:p-8">
  <div class="grid gap-6 lg:grid-cols-[1.2fr_0.8fr]">
    <div>
      <p class="mb-3 text-xs font-semibold uppercase tracking-[0.2em] text-teal-700">Smart Search</p>
      <h1 class="text-3xl font-extrabold text-slate-900 sm:text-4xl">Search books with precision</h1>
      <p class="mt-3 max-w-2xl text-sm text-slate-600 sm:text-base">
        Look up titles and categories in one place, then jump directly into detailed recommendations.
      </p>
      <div class="mt-5 flex flex-wrap gap-2 text-xs sm:text-sm">
        <span class="rounded-full border border-teal-200 bg-teal-50 px-3 py-1 font-semibold text-teal-800">{results.length} results</span>
        <span class="rounded-full border border-orange-200 bg-orange-50 px-3 py-1 font-semibold text-orange-700">{categories.length} quick filters</span>
      </div>
    </div>
    <div class="rounded-2xl border border-white/70 bg-white/75 p-4 shadow-sm">
      <h2 class="text-sm font-bold uppercase tracking-[0.16em] text-slate-500">Quick Tips</h2>
      <ul class="mt-3 space-y-2 text-sm text-slate-600">
        <li>Search by full title or partial keyword.</li>
        <li>Try a category name to browse by theme.</li>
        <li>Open details to get similar recommendations.</li>
      </ul>
    </div>
  </div>
</section>

<section class="panel-surface mb-6 rounded-3xl p-4 sm:p-6">
  <form
    onsubmit={(event) => {
      event.preventDefault();
      doSearch(q);
    }}
    class="flex flex-col gap-3 lg:flex-row lg:items-center"
  >
    <div class="relative flex-1">
      <span class="pointer-events-none absolute left-3 top-3 text-slate-400">⌕</span>
      <input
        type="search"
        bind:value={q}
        placeholder="Search by title or category..."
        class="w-full rounded-2xl border-slate-200 bg-white/85 py-3 pl-10 pr-24 text-sm text-slate-800 placeholder:text-slate-400 focus:border-teal-400 focus:ring-2 focus:ring-teal-200"
      />
      {#if q}
        <button
          type="button"
          onclick={clearSearch}
          class="absolute right-2 top-2 rounded-xl border border-slate-200 px-3 py-1 text-xs font-semibold text-slate-600 hover:border-slate-300 hover:bg-slate-50"
        >
          Clear
        </button>
      {/if}
    </div>
    <button
      type="submit"
      class="rounded-xl border border-teal-700 bg-teal-700 px-5 py-3 text-sm font-semibold text-white transition hover:bg-teal-800"
    >
      Search
    </button>
  </form>

  {#if categories.length > 0}
    <div class="mt-4 flex flex-wrap gap-2">
      {#each categories as c (c)}
        <button
          type="button"
          onclick={() => pickQuick(c)}
          class="rounded-full border border-slate-200 bg-white px-3 py-1.5 text-xs font-semibold capitalize text-slate-700 transition hover:border-teal-300 hover:text-teal-800"
        >
          {c}
        </button>
      {/each}
    </div>
  {/if}
</section>

{#if loading}
  <div class="grid gap-5 sm:grid-cols-2 xl:grid-cols-3 2xl:grid-cols-4">
    {#each skeletonRows as i (i)}
      <article class="animate-pulse rounded-3xl border border-white/70 bg-white/70 p-4 shadow-sm">
        <div class="mb-3 h-48 rounded-2xl bg-slate-200/80"></div>
        <div class="mb-2 h-4 w-3/4 rounded bg-slate-200/80"></div>
        <div class="mb-4 h-4 w-1/2 rounded bg-slate-200/80"></div>
        <div class="h-6 w-20 rounded-full bg-slate-200/80"></div>
      </article>
    {/each}
  </div>
{:else if error}
  <div class="rounded-2xl border border-red-200 bg-red-50 p-5 text-sm text-red-700">
    <span class="font-semibold">Search failed:</span> {error}
  </div>
{:else if results.length === 0 && q.trim().length > 0}
  <div class="rounded-2xl border border-slate-200 bg-white/80 p-8 text-center shadow-sm">
    <h2 class="text-xl font-bold text-slate-900">No books found</h2>
    <p class="mt-2 text-sm text-slate-600">Try a different keyword or choose one of the quick filters.</p>
  </div>
{:else if results.length === 0}
  <div class="rounded-2xl border border-slate-200 bg-white/80 p-8 text-center shadow-sm">
    <h2 class="text-xl font-bold text-slate-900">Start your search</h2>
    <p class="mt-2 text-sm text-slate-600">Enter a title or category to find matching books.</p>
  </div>
{:else}
  <div class="grid gap-5 sm:grid-cols-2 xl:grid-cols-3 2xl:grid-cols-4">
    {#each results as b, i (`${b.slug}-${i}`)}
      <article class="book-card overflow-hidden rounded-3xl">
        <a href={resolve('/books/[slug]', { slug: b.slug })} data-sveltekit-preload-data="hover" class="flex h-full flex-col">
          <div class="book-cover-wrap relative m-3 overflow-hidden rounded-2xl">
            {#if b.img}
              <img src={b.img} alt={b.title} loading="lazy" decoding="async" class="h-full w-full object-contain p-3" />
            {:else}
              <div class="grid h-full place-items-center text-sm text-slate-500">No cover available</div>
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
            <h3 class="title-clamp mb-4 text-base font-bold leading-snug text-slate-900">{b.title}</h3>
            <div class="mt-auto flex items-center justify-between">
              <span class="text-xs font-medium text-slate-500">{b.rating !== null && b.rating !== undefined ? `Rating ${b.rating}/5` : 'Unrated'}</span>
              <span class="rounded-full bg-slate-900 px-3 py-1 text-xs font-semibold text-white">Details</span>
            </div>
          </div>
        </a>
      </article>
    {/each}
  </div>
{/if}
