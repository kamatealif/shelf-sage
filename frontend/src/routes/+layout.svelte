<script>
	import '../app.css';
	import favicon from '$lib/assets/favicon.svg';
	const nav = [
		{ href: '/', label: 'Home' },
		{ href: '/categories', label: 'Categories' },
		{ href: '/search', label: 'Search' },
		{ href: '/about', label: 'About' }
	];

	let { children } = $props();
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
	<link rel="preconnect" href="https://fonts.googleapis.com" />
	<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="anonymous" />
	<link
		href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;700;800&family=Outfit:wght@500;700;800&display=swap"
		rel="stylesheet"
	/>
</svelte:head>

<div class="relative min-h-screen overflow-x-clip">
	<div aria-hidden="true" class="pointer-events-none fixed inset-0 -z-10">
		<div class="absolute -left-28 top-8 h-72 w-72 rounded-full bg-teal-300/40 blur-3xl"></div>
		<div class="absolute -right-24 top-16 h-80 w-80 rounded-full bg-orange-200/55 blur-3xl"></div>
		<div class="absolute bottom-0 left-1/3 h-64 w-64 rounded-full bg-cyan-200/40 blur-3xl"></div>
	</div>

	<header class="sticky top-0 z-40 border-b border-white/45 bg-white/70 backdrop-blur-xl">
		<div class="mx-auto flex max-w-7xl flex-col gap-3 px-4 py-4 sm:px-6 lg:px-8 md:flex-row md:items-center md:justify-between">
			<a href="/" class="flex items-center gap-3">
				<span class="grid h-10 w-10 place-items-center rounded-xl bg-teal-700 text-sm font-extrabold text-white shadow-md shadow-teal-800/25">SS</span>
				<span class="leading-tight">
					<span class="block text-lg font-extrabold text-slate-900">Shelf Sage</span>
					<span class="block text-xs font-medium uppercase tracking-[0.18em] text-slate-500">Book Discovery</span>
				</span>
			</a>
			<nav class="flex flex-wrap items-center gap-2 text-sm font-semibold text-slate-700">
				{#each nav as item}
					<a
						href={item.href}
						class="rounded-full border border-slate-200/80 bg-white/80 px-4 py-1.5 transition-colors hover:border-teal-300 hover:text-teal-800"
					>
						{item.label}
					</a>
				{/each}
			</nav>
		</div>
	</header>

	<main class="mx-auto max-w-7xl px-4 py-8 sm:px-6 md:py-10 lg:px-8">
		{@render children?.()}
	</main>

	<footer class="border-t border-white/55 bg-white/60 py-6 text-center text-sm text-slate-600 backdrop-blur">
		Built by
		<a href="https://kamatealif.github.io" target="_blank" rel="noreferrer" class="font-semibold text-teal-800 underline decoration-teal-500 decoration-2 underline-offset-4">
			Alif Kamate
		</a>
		powered by FastAPI
	</footer>
</div>
