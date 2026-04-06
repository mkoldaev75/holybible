<template>
  <div class="max-w-3xl mx-auto px-4 py-8">
    <!-- Breadcrumb -->
    <nav class="mb-6 text-sm flex items-center gap-2 flex-wrap">
      <router-link :to="'/' + tc" class="text-[#c8b880]/60 hover:text-[#c8b880] transition-colors">←</router-link>
      <span class="text-[#333]">›</span>

      <!-- Book selector -->
      <div class="relative" ref="bookDropRef">
        <button @click="showBookDrop = !showBookDrop"
          class="text-[#c8b880]/60 hover:text-[#c8b880] transition-colors" :dir="dir">
          {{ bookData?.book || bookFile }}
          <span class="text-[10px]">▼</span>
        </button>
        <div v-if="showBookDrop"
          class="absolute left-0 top-full mt-1 w-72 max-h-72 overflow-y-auto rounded-lg bg-[#12121f] border border-[#1a1a2e] shadow-2xl z-50">
          <router-link v-for="b in allBooks" :key="b.file"
            :to="'/' + tc + '/' + b.file.replace('.json','') + '/1'"
            @click="showBookDrop = false"
            class="block px-3 py-1.5 text-sm hover:bg-[#1a1a2e] transition-colors"
            :class="b.file === bookFile + '.json' ? 'text-[#c8b880]' : 'text-[#999]'"
            :dir="dir">
            {{ b.name }}
          </router-link>
        </div>
      </div>

      <span class="text-[#333]">›</span>

      <!-- Chapter selector -->
      <div class="relative" ref="chDropRef">
        <button @click="showChDrop = !showChDrop"
          class="text-[#888] hover:text-[#c8b880] transition-colors font-mono">
          {{ chapter }} <span class="text-[10px]">▼</span>
        </button>
        <div v-if="showChDrop"
          class="absolute left-0 top-full mt-1 w-64 max-h-60 overflow-y-auto rounded-lg bg-[#12121f] border border-[#1a1a2e] shadow-2xl z-50 p-2">
          <div class="grid grid-cols-5 gap-1">
            <router-link v-for="ch in totalChapters" :key="ch"
              :to="'/' + tc + '/' + bookFile + '/' + ch"
              @click="showChDrop = false"
              class="flex items-center justify-center h-9 rounded text-sm font-mono border transition-all"
              :class="ch === chapterNum
                ? 'bg-[#c8b880]/20 border-[#c8b880]/40 text-[#c8b880]'
                : 'bg-[#0d0d14] border-[#1a1a2e] text-[#888] hover:text-[#c8b880] hover:border-[#c8b880]/30'">
              {{ ch }}
            </router-link>
          </div>
        </div>
      </div>
    </nav>

    <!-- Title -->
    <h1 class="text-2xl md:text-3xl font-bold text-[#c8b880] mb-1" :dir="dir">{{ bookData?.book }}</h1>
    <p class="text-[#666] text-lg mb-8">{{ chapter }}</p>

    <!-- Loading -->
    <div v-if="loading" class="text-center py-20 text-[#555]">...</div>
    <div v-else-if="error" class="text-center py-20 text-red-400/60">{{ error }}</div>

    <!-- Verses -->
    <div v-else-if="verses" class="space-y-5 text-2xl leading-relaxed mb-12" :dir="dir">
      <p v-for="verse in verses" :key="verse.verse" class="text-[#d4d0c8]/90">
        <sup class="text-[#c8b880]/50 text-base font-mono mr-1 select-none">{{ verse.verse }}</sup>
        {{ verse.text }}
      </p>
    </div>

    <!-- Prev / Next -->
    <div v-if="verses" class="flex items-center justify-between border-t border-[#1a1a2e] pt-6 mb-8">
      <router-link v-if="hasPrev"
        :to="'/' + tc + '/' + bookFile + '/' + (chapterNum - 1)"
        class="flex items-center gap-2 text-[#c8b880]/70 hover:text-[#c8b880] transition-colors text-sm">
        <span>←</span><span>{{ chapterNum - 1 }}</span>
      </router-link>
      <span v-else></span>

      <router-link :to="'/' + tc"
        class="text-[#555] hover:text-[#888] transition-colors text-xs uppercase tracking-wider font-sans">▦</router-link>

      <router-link v-if="hasNext"
        :to="'/' + tc + '/' + bookFile + '/' + (chapterNum + 1)"
        class="flex items-center gap-2 text-[#c8b880]/70 hover:text-[#c8b880] transition-colors text-sm">
        <span>{{ chapterNum + 1 }}</span><span>→</span>
      </router-link>
      <span v-else></span>
    </div>
  </div>
</template>

<script>
export default {
  props: ['translation', 'bookFile', 'chapter'],
  data() {
    return {
      bookData: null, allBooks: [], rtl: false,
      loading: true, error: null,
      showBookDrop: false, showChDrop: false
    }
  },
  computed: {
    tc() { return this.translation || 'ru_synodal' },
    chapterNum() { return parseInt(this.chapter) },
    totalChapters() { return this.bookData ? Object.keys(this.bookData.chapters).length : 0 },
    hasPrev() { return this.chapterNum > 1 },
    hasNext() { return this.chapterNum < this.totalChapters },
    verses() {
      if (!this.bookData?.chapters) return null
      return this.bookData.chapters[String(this.chapterNum)] || null
    },
    dir() { return this.rtl ? 'rtl' : 'ltr' }
  },
  watch: {
    bookFile() { this.loadBook() },
    chapter() { window.scrollTo(0, 0) }
  },
  methods: {
    async loadBook() {
      this.loading = true
      this.error = null
      try {
        const [bookRes, idxRes, masterRes] = await Promise.all([
          fetch(`/translations/${this.tc}/books/${this.bookFile}.json`),
          fetch(`/translations/${this.tc}/index.json`).then(r => r.json()),
          fetch('/translations/translations.json').then(r => r.json())
        ])
        if (!bookRes.ok) throw new Error(`Not found (${bookRes.status})`)
        this.bookData = await bookRes.json()
        this.allBooks = idxRes.books
        const t = masterRes.translations.find(x => x.code === this.tc)
        this.rtl = t?.rtl || false
      } catch (e) {
        this.error = e.message
      } finally {
        this.loading = false
      }
    },
    onClickOutside(e) {
      if (this.$refs.bookDropRef && !this.$refs.bookDropRef.contains(e.target)) this.showBookDrop = false
      if (this.$refs.chDropRef && !this.$refs.chDropRef.contains(e.target)) this.showChDrop = false
    }
  },
  mounted() {
    this.loadBook()
    document.addEventListener('click', this.onClickOutside)
  },
  beforeUnmount() {
    document.removeEventListener('click', this.onClickOutside)
  }
}
</script>