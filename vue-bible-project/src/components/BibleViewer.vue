<template>
  <div class="max-w-3xl mx-auto p-6">
    <h1 class="text-3xl font-bold mb-8 text-center">{{ data?.book }} — Глава {{ data?.chapter }}</h1>
    <div v-if="data" class="space-y-5 text-lg leading-relaxed">
      <p v-for="verse in data.verses" :key="verse.verse">
        <span class="font-medium text-blue-600">{{ verse.verse }}.</span> {{ verse.text }}
      </p>
    </div>
    <div v-else class="text-center py-12 text-gray-500">Загрузка...</div>
  </div>
</template>

<script>
export default {
  data() { return { data: null } },
  async mounted() {
    try {
      const res = await fetch('/translations/ru_synodal/books/01-GEN/001.json')
      this.data = await res.json()
    } catch (e) {
      console.error(e)
    }
  }
}
</script>
