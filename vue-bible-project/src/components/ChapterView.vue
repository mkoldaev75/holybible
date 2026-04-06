<template>
  <div class="max-w-3xl mx-auto px-4 py-8">
    <!-- Breadcrumb -->
    <nav class="mb-6 text-sm">
      <router-link to="/" class="text-[#c8b880]/60 hover:text-[#c8b880] transition-colors">Книги</router-link>
      <span class="text-[#333] mx-2">›</span>
      <router-link :to="'/' + bookDir" class="text-[#c8b880]/60 hover:text-[#c8b880] transition-colors">
        {{ data?.book || bookDir }}
      </router-link>
      <span class="text-[#333] mx-2">›</span>
      <span class="text-[#888]">Глава {{ chapter }}</span>
    </nav>

    <!-- Header -->
    <h1 class="text-2xl md:text-3xl font-bold text-[#c8b880] mb-1">{{ data?.book }}</h1>
    <p class="text-[#666] text-lg mb-8">Глава {{ chapter }}</p>

    <!-- Loading -->
    <div v-if="loading" class="text-center py-20 text-[#555]">Загрузка...</div>

    <!-- Error -->
    <div v-else-if="error" class="text-center py-20 text-red-400/60">{{ error }}</div>

    <!-- Verses -->
    <div v-else-if="data" class="space-y-4 text-xl leading-relaxed mb-12">
      <p v-for="verse in data.verses" :key="verse.verse" class="text-[#d4d0c8]/90">
        <sup class="text-[#c8b880]/50 text-sm font-mono mr-1 select-none">{{ verse.verse }}</sup>
        {{ verse.text }}
      </p>
    </div>

    <!-- Navigation -->
    <div v-if="data" class="flex items-center justify-between border-t border-[#1a1a2e] pt-6 mb-8">
      <router-link
        v-if="hasPrev"
        :to="'/' + bookDir + '/' + (chapterNum - 1)"
        class="flex items-center gap-2 text-[#c8b880]/70 hover:text-[#c8b880] transition-colors text-sm"
      >
        <span>←</span>
        <span>Глава {{ chapterNum - 1 }}</span>
      </router-link>
      <span v-else></span>

      <router-link
        :to="'/' + bookDir"
        class="text-[#555] hover:text-[#888] transition-colors text-xs uppercase tracking-wider font-sans"
      >
        Все главы
      </router-link>

      <router-link
        v-if="hasNext"
        :to="'/' + bookDir + '/' + (chapterNum + 1)"
        class="flex items-center gap-2 text-[#c8b880]/70 hover:text-[#c8b880] transition-colors text-sm"
      >
        <span>Глава {{ chapterNum + 1 }}</span>
        <span>→</span>
      </router-link>
      <span v-else></span>
    </div>
  </div>
</template>

<script>
export default {
  props: ['bookDir', 'chapter'],
  data() {
    return { data: null, totalChapters: 0, loading: true, error: null }
  },
  computed: {
    chapterNum() { return parseInt(this.chapter) },
    hasPrev() { return this.chapterNum > 1 },
    hasNext() { return this.chapterNum < this.totalChapters },
  },
  watch: {
    chapter() { this.loadChapter() }
  },
  methods: {
    async loadChapter() {
      this.loading = true
      this.error = null
      try {
        const pad = String(this.chapter).padStart(3, '0')
        const url = `/translations/ru_synodal/books/${this.bookDir}/${pad}.json`
        const res = await fetch(url)
        if (!res.ok) throw new Error(`Глава не найдена (${res.status})`)
        this.data = await res.json()

        // Get total chapters for nav
        const idxRes = await fetch('/translations/ru_synodal/index.json')
        const idx = await idxRes.json()
        const book = idx.books.find(b => b.dir === this.bookDir)
        if (book) this.totalChapters = book.chapters
      } catch (e) {
        this.error = e.message
        console.error(e)
      } finally {
        this.loading = false
      }
    }
  },
  mounted() {
    this.loadChapter()
  }
}
</script>
