<script>
	import '../app.css';
	import favicon from '$lib/assets/favicon.svg';

	let { children, data } = $props();
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
</svelte:head>

<header class="bg-white shadow">
  <div class="container flex items-center justify-between py-4">
    <a href="/" class="text-2xl font-bold">📚 Shelf Sage</a>
    <nav class="flex gap-4 text-sm">
      <a href="/" class="hover:underline">Home</a>
      <a href="/categories" class="hover:underline">Categories</a>
      <a href="/search" class="hover:underline">Search</a>
      <a href="/about" class="hover:underline">About</a>
    </nav>
  </div>
</header>

<main class="container py-8">
{@render children?.()}
</main>



<footer class="text-center py-6 text-sm text-gray-600">
  Built by <a href="https://kamatealif.github.io" target="_blank" rel="noreferrer" class="underline">Alif Kamate</a> — powered by FastAPI
</footer>