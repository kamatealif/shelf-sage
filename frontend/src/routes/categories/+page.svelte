<script>
  import { onMount } from 'svelte';
  import { fetchCategories } from '$lib/api';

  let cats = [];
  let error = null;

  onMount(async () => {
    try {
      cats = await fetchCategories();
    } catch (e) {
      console.error(e);
      error = e.message;
    }
  });
</script>

<h1 class="text-2xl font-semibold mb-4">Categories</h1>

{#if error}
  <div class="text-red-600">Error: {error}</div>
{:else}
  <ul class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4">
    {#each cats as c}
      <li class="bg-white p-4 rounded shadow hover:shadow-md">
        <a href={`/search?q=${encodeURIComponent(c)}`} class="block capitalize">{c}</a>
      </li>
    {/each}
  </ul>
{/if}
