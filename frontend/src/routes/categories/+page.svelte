<script>
  import { onMount } from 'svelte';
  import { resolve } from '$app/paths';
  import { fetchCategories } from '$lib/api';

  let cats = [];
  let loading = true;
  let error = null;
  let filter = '';
  const skeletonRows = Array.from({ length: 8 }, (_, i) => i);

  onMount(async () => {
    loading = true;
    error = null;
    try {
      cats = await fetchCategories();
    } catch (e) {
      error = e?.body?.detail || e?.message || 'Failed to load categories';
    } finally {
      loading = false;
    }
  });

  $: needle = filter.trim().toLowerCase();
  $: visibleCats = needle ? cats.filter((c) => c.includes(needle)) : cats;
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

  .category-card {
    border: 1px solid var(--stroke);
    background: var(--surface-strong);
    box-shadow: 0 10px 24px rgba(15, 23, 42, 0.07);
    transition: transform 0.22s ease, box-shadow 0.22s ease, border-color 0.22s ease;
  }

  .category-card:hover {
    transform: translateY(-3px);
    border-color: rgba(13, 148, 136, 0.35);
    box-shadow: 0 18px 32px rgba(15, 23, 42, 0.1);
  }
</style>

<section class="hero-surface mb-6 rounded-3xl p-6 sm:p-8">
  <div class="grid gap-6 lg:grid-cols-[1.2fr_0.8fr]">
    <div>
      <p class="mb-3 text-xs font-semibold uppercase tracking-[0.2em] text-teal-700">Category Explorer</p>
      <h1 class="text-3xl font-extrabold text-slate-900 sm:text-4xl">Browse by category</h1>
      <p class="mt-3 max-w-2xl text-sm text-slate-600 sm:text-base">
        Jump straight into a theme and open curated matches in search with one click.
      </p>
      <div class="mt-5 flex flex-wrap gap-2 text-xs sm:text-sm">
        <span class="rounded-full border border-teal-200 bg-teal-50 px-3 py-1 font-semibold text-teal-800">{cats.length} categories</span>
        <span class="rounded-full border border-slate-200 bg-white px-3 py-1 font-semibold text-slate-700">{visibleCats.length} visible</span>
      </div>
    </div>
    <div class="rounded-2xl border border-white/70 bg-white/75 p-4 shadow-sm">
      <h2 class="text-sm font-bold uppercase tracking-[0.16em] text-slate-500">How to use</h2>
      <ul class="mt-3 space-y-2 text-sm text-slate-600">
        <li>Use the filter to quickly find a category.</li>
        <li>Tap open search to jump into matching titles.</li>
        <li>Open any book card for detailed recommendations.</li>
      </ul>
    </div>
  </div>
</section>

<section class="panel-surface mb-6 rounded-3xl p-4 sm:p-6">
  <label for="category-filter" class="mb-2 block text-xs font-semibold uppercase tracking-[0.16em] text-slate-500">Find category</label>
  <input
    id="category-filter"
    type="search"
    bind:value={filter}
    placeholder="Type category name..."
    class="w-full rounded-2xl border-slate-200 bg-white/85 px-4 py-3 text-sm text-slate-800 placeholder:text-slate-400 focus:border-teal-400 focus:ring-2 focus:ring-teal-200"
  />
</section>

{#if loading}
  <div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
    {#each skeletonRows as i (i)}
      <div class="animate-pulse rounded-2xl border border-white/70 bg-white/70 p-4 shadow-sm">
        <div class="mb-3 h-4 w-2/3 rounded bg-slate-200/80"></div>
        <div class="h-3 w-1/2 rounded bg-slate-200/80"></div>
      </div>
    {/each}
  </div>
{:else if error}
  <div class="rounded-2xl border border-red-200 bg-red-50 p-5 text-sm text-red-700">
    <span class="font-semibold">Request failed:</span> {error}
  </div>
{:else if visibleCats.length === 0}
  <div class="rounded-2xl border border-slate-200 bg-white/80 p-8 text-center shadow-sm">
    <h2 class="text-xl font-bold text-slate-900">No categories match</h2>
    <p class="mt-2 text-sm text-slate-600">Try a different keyword in the filter.</p>
  </div>
{:else}
  <div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
    {#each visibleCats as c (c)}
      <article class="category-card rounded-2xl p-4">
        <h3 class="mb-2 text-base font-bold capitalize text-slate-900">{c}</h3>
        <p class="mb-4 text-xs text-slate-500">Open focused search results for this category.</p>
        <form action={resolve('/search')} method="GET">
          <input type="hidden" name="q" value={c} />
          <button
            type="submit"
            class="inline-flex items-center rounded-xl border border-teal-700 bg-teal-700 px-3 py-1.5 text-xs font-semibold text-white transition hover:bg-teal-800"
          >
            Open search
          </button>
        </form>
      </article>
    {/each}
  </div>
{/if}
