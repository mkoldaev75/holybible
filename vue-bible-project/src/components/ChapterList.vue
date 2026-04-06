<template>
  <div class="max-w-4xl mx-auto px-4 py-8">
    <!-- Breadcrumb -->
    <nav class="mb-6 text-sm">
      <router-link to="/" class="text-[#c8b880]/60 hover:text-[#c8b880] transition-colors">Книги</router-link>
      <span class="text-[#333] mx-2">›</span>
      <span class="text-[#888]">{{ bookName }}</span>
    </nav>

    <h1 class="text-3xl md:text-4xl font-bold text-[#c8b880] mb-8">{{ bookName }}</h1>

    <div v-if="loading" class="text-center py-20 text-[#555]">Загрузка...</div>

    <div v-else>
      <p class="text-xs uppercase tracking-[0.3em] text-[#555] mb-4 font-sans">Выберите главу</p>
      <div class="grid gap-2" :class="gridClass">
        <router-link
          v-for="ch in totalChapters"
          :key="ch"
          :to="'/' + bookDir + '/' + ch"
          class="flex items-center justify-center h-12 rounded bg-[#12121f] hover:bg-[#1a1a2e] text-[#d4d0c8] hover:text-[#c8b880] transition-all text-lg font-mono border border-[#1a1a2e] hover:border-[#c8b880]/30"
        >
          {{ ch }}
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: ['bookDir'],
  data() {
    return { bookName: '', totalChapters: 0, loading: true }
  },
  computed: {
    gridClass() {
      if (this.totalChapters <= 5) return 'grid-cols-5'
      if (this.totalChapters <= 10) return 'grid-cols-5 sm:grid-cols-10'
      return 'grid-cols-5 sm:grid-cols-10'
    }
  },
  async mounted() {
    try {
      const res = await fetch('/translations/ru_synodal/index.json')
      const data = await res.json()
      const book = data.books.find(b => b.dir === this.bookDir)
      if (book) {
        this.bookName = book.name
        this.totalChapters = book.chapters
      }
    } catch (e) {
      console.error(e)
    } finally {
      this.loading = false
    }
  }
}
</script>
