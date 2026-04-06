<template>
  <div class="max-w-4xl mx-auto px-4 py-8">
    <h1 class="text-4xl md:text-5xl font-bold text-center text-[#c8b880] mb-2 tracking-wide">
      Священное Писание
    </h1>
    <p class="text-center text-[#666] text-lg mb-10">Синодальный перевод</p>

    <div v-if="loading" class="text-center py-20 text-[#555]">Загрузка...</div>

    <template v-else>
      <!-- Ветхий Завет -->
      <section class="mb-10">
        <h2 class="text-xs uppercase tracking-[0.3em] text-[#c8b880]/60 mb-4 font-sans font-semibold border-b border-[#1a1a2e] pb-2">
          Ветхий Завет
        </h2>
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-1">
          <router-link
            v-for="book in otBooks"
            :key="book.dir"
            :to="'/' + book.dir"
            class="group flex items-baseline gap-3 px-3 py-2.5 rounded hover:bg-[#12121f] transition-colors"
          >
            <span class="text-xs text-[#555] font-mono w-5 text-right shrink-0">{{ book.number }}</span>
            <span class="text-[#d4d0c8] group-hover:text-[#c8b880] transition-colors text-lg">
              {{ shortName(book.name) }}
            </span>
            <span class="text-xs text-[#444] ml-auto font-mono">{{ book.chapters }}</span>
          </router-link>
        </div>
      </section>

      <!-- Новый Завет -->
      <section>
        <h2 class="text-xs uppercase tracking-[0.3em] text-[#c8b880]/60 mb-4 font-sans font-semibold border-b border-[#1a1a2e] pb-2">
          Новый Завет
        </h2>
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-1">
          <router-link
            v-for="book in ntBooks"
            :key="book.dir"
            :to="'/' + book.dir"
            class="group flex items-baseline gap-3 px-3 py-2.5 rounded hover:bg-[#12121f] transition-colors"
          >
            <span class="text-xs text-[#555] font-mono w-5 text-right shrink-0">{{ book.number }}</span>
            <span class="text-[#d4d0c8] group-hover:text-[#c8b880] transition-colors text-lg">
              {{ shortName(book.name) }}
            </span>
            <span class="text-xs text-[#444] ml-auto font-mono">{{ book.chapters }}</span>
          </router-link>
        </div>
      </section>
    </template>
  </div>
</template>

<script>
export default {
  data() {
    return { books: [], loading: true }
  },
  computed: {
    otBooks() { return this.books.filter(b => b.number <= 39) },
    ntBooks() { return this.books.filter(b => b.number > 39) },
  },
  methods: {
    shortName(name) {
      // Убираем "КНИГА ПРОРОКА ", "КНИГА " и подобные длинные префиксы для компактности
      return name
        .replace(/^КНИГА ПРОРОКА\s+/i, '')
        .replace(/^КНИГА ПЛАЧ\s+/i, 'Плач ')
        .replace(/^КНИГА ПЕСНИ ПЕСНЕЙ\s+/i, 'Песнь Песней ')
        .replace(/^КНИГА ПРИТЧЕЙ\s+/i, 'Притчи ')
        .replace(/^КНИГА ЕККЛЕЗИАСТА.*/i, 'Екклезиаст')
        .replace(/^КНИГА\s+/i, '')
        .replace(/^ПЕРВАЯ КНИГА МОИСЕЕВА:\s*/i, 'Бытие')
        .replace(/^ВТОРАЯ КНИГА МОИСЕЕВА:\s*/i, 'Исход')
        .replace(/^ТРЕТЬЯ КНИГА МОИСЕЕВА:\s*/i, 'Левит')
        .replace(/^ЧЕТВЕРТАЯ КНИГА МОИСЕЕВА:\s*/i, 'Числа')
        .replace(/^ПЯТАЯ КНИГА МОИСЕЕВА:\s*/i, 'Второзаконие')
        .replace(/СВЯТОЕ БЛАГОВЕСТВОВАНИЕ/i, '')
        .replace(/СВЯТОГО АПОСТОЛА ПАВЛА/i, '')
        .replace(/СВЯТОГО АПОСТОЛА/i, '')
        .replace(/СВЯТЫХ АПОСТОЛОВ/i, '')
        .replace(/СОБОРНОЕ ПОСЛАНИЕ/i, 'Послание')
        .replace(/ПЕРВОЕ СОБОРНОЕ ПОСЛАНИЕ/i, '1-е послание')
        .replace(/ВТОРОЕ СОБОРНОЕ ПОСЛАНИЕ/i, '2-е послание')
        .replace(/ТРЕТЬЕ СОБОРНОЕ ПОСЛАНИЕ/i, '3-е послание')
        .replace(/\s{2,}/g, ' ')
        .trim()
    }
  },
  async mounted() {
    try {
      const res = await fetch('/translations/ru_synodal/index.json')
      const data = await res.json()
      this.books = data.books
    } catch (e) {
      console.error('Failed to load index:', e)
    } finally {
      this.loading = false
    }
  }
}
</script>
