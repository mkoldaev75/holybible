<template>
  <div class="max-w-4xl mx-auto px-4 py-8">
    <h1 class="text-4xl md:text-5xl font-bold text-center text-[#c8b880] mb-2 tracking-wide">
      {{ langName }}
    </h1>
    <p class="text-center text-[#666] text-lg mb-10">{{ tc }}</p>

    <div v-if="loading" class="text-center py-20 text-[#555]">...</div>

    <template v-else-if="books.length">
      <section class="mb-10">
        <h2 class="text-xs uppercase tracking-[0.3em] text-[#c8b880]/60 mb-4 font-sans font-semibold border-b border-[#1a1a2e] pb-2">
          Old Testament
        </h2>
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-1">
          <router-link
            v-for="book in otBooks" :key="book.file"
            :to="'/' + tc + '/' + bookSlug(book) + '/1'"
            class="group flex items-baseline gap-3 px-3 py-2.5 rounded hover:bg-[#12121f] transition-colors"
          >
            <span class="text-sm text-[#555] font-mono w-5 text-right shrink-0">{{ book.number }}</span>
            <span class="text-[#d4d0c8] group-hover:text-[#c8b880] transition-colors text-xl" :dir="rtl ? 'rtl' : 'ltr'">{{ book.name }}</span>
            <span class="text-sm text-[#444] ml-auto font-mono">{{ book.chapters }}</span>
          </router-link>
        </div>
      </section>

      <section>
        <h2 class="text-xs uppercase tracking-[0.3em] text-[#c8b880]/60 mb-4 font-sans font-semibold border-b border-[#1a1a2e] pb-2">
          New Testament
        </h2>
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-1">
          <router-link
            v-for="book in ntBooks" :key="book.file"
            :to="'/' + tc + '/' + bookSlug(book) + '/1'"
            class="group flex items-baseline gap-3 px-3 py-2.5 rounded hover:bg-[#12121f] transition-colors"
          >
            <span class="text-sm text-[#555] font-mono w-5 text-right shrink-0">{{ book.number }}</span>
            <span class="text-[#d4d0c8] group-hover:text-[#c8b880] transition-colors text-xl" :dir="rtl ? 'rtl' : 'ltr'">{{ book.name }}</span>
            <span class="text-sm text-[#444] ml-auto font-mono">{{ book.chapters }}</span>
          </router-link>
        </div>
      </section>
    </template>
  </div>
</template>

<script>
export default {
  props: { translation: { type: String, default: 'ru_synodal' } },
  data() { return { books: [], rtl: false, langName: '', loading: true } },
  computed: {
    tc() { return this.translation || 'ru_synodal' },
    otBooks() { return this.books.filter(b => b.number <= 39) },
    ntBooks() { return this.books.filter(b => b.number > 39) },
  },
  watch: { translation() { this.load() } },
  mounted() { this.load() },
  methods: {
    bookSlug(book) { return book.file.replace('.json', '') },
    async load() {
      this.loading = true
      try {
        const [idx, master] = await Promise.all([
          fetch(`/translations/${this.tc}/index.json`).then(r => r.json()),
          fetch('/translations/translations.json').then(r => r.json())
        ])
        this.books = idx.books
        const t = master.translations.find(x => x.code === this.tc)
        this.rtl = t?.rtl || false
        this.langName = t?.name || this.tc
      } catch (e) { console.error(e) }
      finally { this.loading = false }
    }
  }
}
</script>