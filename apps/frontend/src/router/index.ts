import { createRouter, createWebHistory } from 'vue-router';

import ApiDocsPage from '../pages/ApiDocsPage.vue';
import DocumentPage from '../pages/DocumentPage.vue';
import DocumentsPage from '../pages/DocumentsPage.vue';
import SearchPage from '../pages/SearchPage.vue';
import UploadPage from '../pages/UploadPage.vue';

export const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: SearchPage },
    { path: '/documents', component: DocumentsPage },
    { path: '/upload', component: UploadPage },
    { path: '/api-docs', component: ApiDocsPage },
    { path: '/documents/:id', component: DocumentPage },
  ],
});

