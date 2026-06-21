import { defineStore } from 'pinia';

import { searchDocuments, type SearchResult } from '../services/api';

export const useSearchStore = defineStore('search', {
  state: () => ({
    query: '',
    results: [] as SearchResult[],
    loading: false,
    error: '',
  }),
  actions: {
    async search(query: string) {
      this.query = query;
      this.loading = true;
      this.error = '';

      try {
        const response = await searchDocuments(query);
        this.results = response.items;
      } catch (error) {
        this.error = error instanceof Error ? error.message : 'Search failed';
      } finally {
        this.loading = false;
      }
    },
  },
});

