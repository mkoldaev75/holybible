<template>
  <div class="min-h-screen bg-[#0a0a0f] text-[#d4d0c8]">
    <header class="border-b border-[#1a1a2e] bg-[#0d0d14]/80 backdrop-blur-sm sticky top-0 z-50">
      <div class="max-w-4xl mx-auto px-4 py-3 flex items-center gap-3">
        <router-link to="/" class="flex items-center gap-2 text-[#c8b880] hover:text-[#e0d4a8] transition-colors">
          <span class="text-xl">✝</span>
          <span class="font-semibold tracking-wide text-sm uppercase">Библия</span>
        </router-link>
        <span class="text-[#333] text-xs">Синодальный перевод</span>
      </div>
    </header>
    <main>
      <router-view />
    </main>
  </div>
</template>