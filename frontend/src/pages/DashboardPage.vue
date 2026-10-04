<template>
  <div class="min-h-screen bg-slate-100 p-8">
    <div class="mx-auto max-w-4xl">
      <div class="rounded-2xl bg-white p-8 shadow-xl">
        Dashboard
        <h1 class="text-4xl font-bold text-blue-600">
          Tailwind CSS Test
        </h1>

        <p class="mt-3 text-lg text-slate-600">
          If you can see this styled correctly, Tailwind CSS is working.
        </p>

        <div class="mt-8 grid gap-4 sm:grid-cols-3">
          <div class="rounded-xl bg-blue-100 p-6">
            <p class="text-2xl font-bold text-blue-700">
              FLEX
            </p>
            <p class="mt-2 text-sm text-blue-600">
              Tailwind layout
            </p>
          </div>

          <div class="rounded-xl bg-green-100 p-6">
            <p class="text-2xl font-bold text-green-700">
              GRID
            </p>
            <p class="mt-2 text-sm text-green-600">
              Tailwind responsive grid
            </p>
          </div>

          <div class="rounded-xl bg-purple-100 p-6">
            <p class="text-2xl font-bold text-purple-700">
              SPACING
            </p>
            <p class="mt-2 text-sm text-purple-600">
              Tailwind padding/gap
            </p>
          </div>
        </div>

        <div class="mt-8 flex flex-wrap items-center gap-4">
          <button
            class="rounded-lg bg-blue-600 px-5 py-3 font-semibold text-white hover:bg-blue-700"
          >
            Tailwind Button
          </button>

          <span
            class="rounded-full bg-green-100 px-4 py-2 text-sm font-semibold text-green-700"
          >
            Tailwind is working
          </span>
        </div>
      </div>
    </div>
  </div>
</template>