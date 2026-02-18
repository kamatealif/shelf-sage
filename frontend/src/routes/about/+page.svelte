<script>
  import { resolve } from '$app/paths';

  const stack = [
    { name: 'FastAPI', detail: 'Typed REST API with recommendation endpoints.' },
    { name: 'SvelteKit', detail: 'Modern frontend with route-driven UI and SSR.' },
    { name: 'Pandas', detail: 'Dataset processing and feature preparation.' },
    { name: 'Category Model', detail: 'Practical recommendation baseline by content grouping.' }
  ];
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

  .stack-card {
    border: 1px solid var(--stroke);
    background: var(--surface-strong);
    box-shadow: 0 10px 24px rgba(15, 23, 42, 0.07);
    transition: transform 0.22s ease, box-shadow 0.22s ease;
  }

  .stack-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 16px 30px rgba(15, 23, 42, 0.11);
  }
</style>

<section class="hero-surface mb-6 rounded-3xl p-6 sm:p-8">
  <div class="grid gap-6 lg:grid-cols-[1.2fr_0.8fr]">
    <div>
      <p class="mb-3 text-xs font-semibold uppercase tracking-[0.2em] text-teal-700">About Shelf Sage</p>
      <h1 class="text-3xl font-extrabold text-slate-900 sm:text-4xl">Book discovery, built with practical ML</h1>
      <p class="mt-3 max-w-2xl text-sm text-slate-600 sm:text-base">
        Shelf Sage is a full-stack book recommendation project focused on clean data, reliable APIs,
        and a modern browsing experience for one thousand curated books.
      </p>
      <div class="mt-5 flex flex-wrap gap-2 text-xs sm:text-sm">
        <span class="rounded-full border border-teal-200 bg-teal-50 px-3 py-1 font-semibold text-teal-800">1000 books</span>
        <span class="rounded-full border border-slate-200 bg-white px-3 py-1 font-semibold text-slate-700">FastAPI + SvelteKit</span>
      </div>
    </div>
    <div class="rounded-2xl border border-white/70 bg-white/75 p-4 shadow-sm">
      <h2 class="text-sm font-bold uppercase tracking-[0.16em] text-slate-500">Project Goals</h2>
      <ul class="mt-3 space-y-2 text-sm text-slate-600">
        <li>Deliver useful recommendations with transparent logic.</li>
        <li>Keep the API simple, debuggable, and production-friendly.</li>
        <li>Provide a fast, polished UI for exploration and search.</li>
      </ul>
    </div>
  </div>
</section>

<section class="panel-surface mb-6 rounded-3xl p-5 sm:p-6">
  <h2 class="text-xl font-bold text-slate-900">Tech Stack</h2>
  <p class="mt-1 text-sm text-slate-600">Core technologies powering data, recommendations, and frontend experience.</p>

  <div class="mt-5 grid gap-4 sm:grid-cols-2">
    {#each stack as item (item.name)}
      <article class="stack-card rounded-2xl p-4">
        <h3 class="text-base font-bold text-slate-900">{item.name}</h3>
        <p class="mt-2 text-sm text-slate-600">{item.detail}</p>
      </article>
    {/each}
  </div>
</section>

<section class="panel-surface rounded-3xl p-5 sm:p-6">
  <h2 class="text-xl font-bold text-slate-900">Author & Links</h2>
  <p class="mt-2 text-sm text-slate-600">
    Built by Alif Kamate as a practical recommendation system from scraping to interface.
  </p>

  <div class="mt-5 flex flex-wrap gap-3">
    <a
      href="https://github.com/kamatealif/shelf-sage"
      target="_blank"
      rel="noreferrer"
      class="rounded-xl border border-slate-300 bg-white px-4 py-2 text-sm font-semibold text-slate-800 transition hover:border-teal-300 hover:text-teal-800"
    >
      View on GitHub
    </a>
    <a
      href="https://kamatealif.github.io"
      target="_blank"
      rel="noreferrer"
      class="rounded-xl border border-teal-700 bg-teal-700 px-4 py-2 text-sm font-semibold text-white transition hover:bg-teal-800"
    >
      Author Portfolio
    </a>
    <a
      href={resolve('/')}
      class="rounded-xl border border-slate-300 bg-white px-4 py-2 text-sm font-semibold text-slate-800 transition hover:border-teal-300 hover:text-teal-800"
    >
      Back to Home
    </a>
  </div>
</section>
