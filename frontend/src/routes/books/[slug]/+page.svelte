<script>
  import { resolve } from '$app/paths';

  let { data } = $props();
  let detail = $derived(data?.book ?? null);
  let recommendations = $derived(data?.recommendations ?? []);

  function formatPrice(price) {
    if (price === null || price === undefined || Number.isNaN(Number(price))) return 'Price N/A';
    return `£${Number(price).toFixed(2)}`;
  }
</script>

<style>
  .detail-surface {
    background:
      linear-gradient(150deg, rgba(255, 255, 255, 0.88), rgba(240, 253, 250, 0.72)),
      linear-gradient(0deg, rgba(255, 255, 255, 0.45), rgba(255, 255, 255, 0.45));
    border: 1px solid var(--stroke);
    box-shadow: 0 20px 42px rgba(15, 23, 42, 0.08);
  }

  .rec-card {
    border: 1px solid var(--stroke);
    box-shadow: 0 10px 22px rgba(15, 23, 42, 0.07);
    transition: transform 0.22s ease, box-shadow 0.22s ease, border-color 0.22s ease;
  }

  .rec-card:hover {
    transform: translateY(-3px);
    border-color: rgba(13, 148, 136, 0.35);
    box-shadow: 0 16px 28px rgba(15, 23, 42, 0.1);
  }

  .title-clamp {
    display: -webkit-box;
    overflow: hidden;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
  }
</style>

{#if !detail}
  <div class="rounded-2xl border border-slate-200 bg-white/80 p-8 text-center shadow-sm">
    <h2 class="text-xl font-bold text-slate-900">Book not found</h2>
    <p class="mt-2 text-sm text-slate-600">This book could not be loaded.</p>
    <a href={resolve('/')} class="mt-4 inline-block rounded-xl border border-teal-700 bg-teal-700 px-4 py-2 text-sm font-semibold text-white hover:bg-teal-800">
      Back to home
    </a>
  </div>
{:else}
  <section class="detail-surface mb-8 rounded-3xl p-5 sm:p-6">
    <div class="mb-5 flex flex-wrap items-center justify-between gap-3">
      <a
        href={resolve('/')}
        class="inline-flex items-center rounded-full border border-slate-200 bg-white px-3 py-1.5 text-xs font-semibold uppercase tracking-wide text-slate-700 transition hover:border-teal-300 hover:text-teal-800"
      >
        Back to Home
      </a>
      <span class="rounded-full border border-orange-200 bg-orange-50 px-3 py-1 text-xs font-semibold text-orange-700">
        {recommendations.length} recommendations
      </span>
    </div>

    <div class="grid gap-6 md:grid-cols-[260px_1fr]">
      <div class="overflow-hidden rounded-2xl bg-slate-100/80 p-3">
        {#if detail.img}
          <img src={detail.img} alt={detail.title} class="h-full w-full object-contain" loading="lazy" decoding="async" />
        {:else}
          <div class="grid h-64 place-items-center text-sm text-slate-500">No cover available</div>
        {/if}
      </div>
      <div>
        <p class="mb-2 text-xs font-semibold uppercase tracking-[0.16em] text-teal-700">Selected Book</p>
        <h1 class="text-2xl font-extrabold leading-tight text-slate-900 sm:text-3xl">{detail.title}</h1>
        <div class="mt-3 flex flex-wrap gap-2 text-xs sm:text-sm">
          <span class="rounded-full bg-teal-50 px-3 py-1 font-semibold capitalize text-teal-700">{detail.category}</span>
          <span class="rounded-full bg-slate-100 px-3 py-1 font-semibold text-slate-700">Rating {detail.rating ?? '-'}/5</span>
          <span class="rounded-full bg-orange-50 px-3 py-1 font-semibold text-orange-700">{formatPrice(detail.price_clean)}</span>
        </div>
        <p class="mt-5 whitespace-pre-line text-sm leading-relaxed text-slate-700">
          {detail.description || 'No description available.'}
        </p>
      </div>
    </div>
  </section>

  <section class="detail-surface rounded-3xl p-5 sm:p-6">
    <h2 class="text-xl font-bold text-slate-900">Recommended Books</h2>
    <p class="mt-1 text-sm text-slate-600">Discover similar books below this detail card.</p>

    {#if recommendations.length === 0}
      <p class="mt-4 text-sm text-slate-600">No recommendations available for this book.</p>
    {:else}
      <div class="mt-5 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {#each recommendations as rec (rec.slug)}
          <a
            href={resolve('/books/[slug]', { slug: rec.slug })}
            data-sveltekit-preload-data="hover"
            class="rec-card flex gap-3 rounded-2xl bg-white p-3"
          >
            <div class="grid h-28 w-20 shrink-0 place-items-center overflow-hidden rounded-xl bg-slate-100">
              {#if rec.img}
                <img src={rec.img} alt={rec.title} class="h-full w-full object-contain" loading="lazy" decoding="async" />
              {:else}
                <span class="text-xs text-slate-500">No image</span>
              {/if}
            </div>
            <div class="min-w-0">
              <h3 class="title-clamp text-sm font-bold text-slate-900">{rec.title}</h3>
              <p class="mt-1 text-xs capitalize text-slate-500">{rec.category}</p>
              <p class="mt-2 text-xs text-slate-600">Rating {rec.rating ?? '-'}/5</p>
              <p class="mt-1 text-sm font-semibold text-slate-900">{formatPrice(rec.price_clean)}</p>
            </div>
          </a>
        {/each}
      </div>
    {/if}
  </section>
{/if}
