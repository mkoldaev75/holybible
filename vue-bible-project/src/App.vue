<template>
  <div class="min-h-screen bg-[#0a0a0f] text-[#d4d0c8]">
    <header class="border-b border-[#1a1a2e] bg-[#0d0d14]/80 backdrop-blur-sm sticky top-0 z-50">
      <div class="max-w-4xl mx-auto px-4 py-3 flex items-center gap-3">
        <router-link to="/" class="flex items-center gap-2 text-[#c8b880] hover:text-[#e0d4a8] transition-colors shrink-0">
          <span class="text-xl">✝</span>
          <span class="font-semibold tracking-wide text-sm uppercase hidden sm:inline">Holy Bible</span>
        </router-link>
        <div class="ml-auto relative" ref="dropdownRef">
          <button
            @click="showLangs = !showLangs"
            class="flex items-center gap-1.5 px-3 py-1.5 rounded bg-[#12121f] border border-[#1a1a2e] hover:border-[#c8b880]/30 text-sm text-[#999] hover:text-[#c8b880] transition-all"
          >
            <span>{{ currentLangName }}</span>
            <span class="text-[10px]">▼</span>
          </button>
          <div
            v-if="showLangs"
            class="absolute right-0 top-full mt-1 w-64 max-h-80 overflow-y-auto rounded-lg bg-[#12121f] border border-[#1a1a2e] shadow-2xl z-50"
          >
            <router-link
              v-for="t in translations"
              :key="t.code"
              :to="'/' + t.code"
              @click="showLangs = false"
              class="flex items-center gap-2 px-3 py-2 text-sm hover:bg-[#1a1a2e] transition-colors"
              :class="t.code === currentTranslation ? 'text-[#c8b880]' : 'text-[#999]'"
            >
              <span class="w-8 text-[#555] font-mono text-xs">{{ t.language }}</span>
              <span>{{ t.name }}</span>
              <span v-if="t.books === 0" class="ml-auto text-[10px] text-[#555]">пусто</span>
            </router-link>
          </div>
        </div>
      </div>
    </header>
    <main>
      <router-view :key="$route.fullPath" />
    </main>
  </div>
</template>

<script>
export default {
  data() {
    return { translations: [], showLangs: false }
  },
  computed: {
    currentTranslation() {
      return this.$route.params.translation || 'ru_synodal'
    },
    currentLangName() {
      const t = this.translations.find(x => x.code === this.currentTranslation)
      return t ? t.name : 'Язык'
    }
  },
  methods: {
    onClickOutside(e) {
      if (this.$refs.dropdownRef && !this.$refs.dropdownRef.contains(e.target)) {
        this.showLangs = false
      }
    }
  },
  async mounted() {
    try {
      const res = await fetch('/translations/translations.json')
      const data = await res.json()
      this.translations = data.translations.filter(t => t.books > 0)
    } catch (e) {
      console.error(e)
    }
    document.addEventListener('click', this.onClickOutside)
  },
  beforeUnmount() {
    document.removeEventListener('click', this.onClickOutside)
  }
}
</script>