<script>
  import { onMount } from 'svelte';
  import { page } from '$app/stores';
  import { searchBooks } from '$lib/api';
  import { get } from 'svelte/store';

  let q = '';
  let results = [];
  let loading = false;

  // read ?q= from URL
  onMount(async () => {
    const qp = get(page).url.searchParams.get('q') || '';
    if (qp) {
      q = qp;
      await doSearch(q);
    }
  });

  async function doSearch(query) {
    loading = true;
    try {
      results = await searchBooks(query);
    } catch (e) {
      console.error(e);
      alert('Search failed');
    } finally {
      loading = false;
    }
  }
</script>

<h1 class="text-2xl font-semibold mb-4">Search</h1>

<form on:submit|preventDefault={() => doSearch(q)} class="mb-4">
  <input type="text" bind:value={q} placeholder="Search books..." class="border px-3 py-2 mr-2" />
  <button class="px-4 py-2 bg-blue-500 text-white rounded">Search</button>
</form>

{#if loading}
  <div>Loading...</div>
{:else}
  <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
    {#each results as b}
      <a href={`/books/${b.slug}`} class="bg-white p-4 rounded shadow hover:shadow-md">
        <h3 class="font-medium">{b.title}</h3>
        <div class="text-xs text-gray-500">{b.category}</div>
      </a>
    {/each}
  </div>
{/if}
{#if !loading && results.length === 0 && q}
  <div class="text-gray-600 mt-4">No results found for "{q}"</div>
{/if}