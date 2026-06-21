import { createI18n } from 'vue-i18n';

export type Locale = 'en' | 'ru';

const storageKey = 'locascan.locale';

export const messages = {
  en: {
    nav: {
      search: 'Search',
      upload: 'Upload',
      language: 'Language',
    },
    search: {
      placeholder: 'Search local documents',
      button: 'Search',
    },
    upload: {
      title: 'Upload Documents',
      tabs: {
        pdf: 'PDF',
        images: 'Images',
        office: 'Office',
        text: 'Text/Markdown',
      },
      choosePdf: 'Choose PDF',
      chooseImage: 'Choose image',
      chooseOffice: 'Choose office file',
      chooseText: 'Choose text/Markdown',
      scannerOcr: 'Top scanner OCR',
      ocrModel: 'OCR model via OpenAI API',
      upload: 'Upload',
      uploadWithOcr: 'Upload with OCR model',
      uploadWithParser: 'Upload with parser',
      uploadText: 'Upload text',
      chooseFileFirst: 'Choose a file first.',
      uploaded: 'Uploaded {name}; document id {id}',
    },
    document: {
      recognized: 'Recognized Document',
      downloadOriginal: 'Download original',
    },
    errors: {
      searchFailed: 'Search failed',
    },
  },
  ru: {
    nav: {
      search: 'Поиск',
      upload: 'Загрузка',
      language: 'Язык',
    },
    search: {
      placeholder: 'Поиск по локальным документам',
      button: 'Найти',
    },
    upload: {
      title: 'Загрузка документов',
      tabs: {
        pdf: 'PDF',
        images: 'Изображения',
        office: 'Office',
        text: 'Текст/Markdown',
      },
      choosePdf: 'Выбрать PDF',
      chooseImage: 'Выбрать изображение',
      chooseOffice: 'Выбрать офисный файл',
      chooseText: 'Выбрать текст/Markdown',
      scannerOcr: 'Лучший сканер OCR',
      ocrModel: 'OCR модель через OpenAI API',
      upload: 'Загрузить',
      uploadWithOcr: 'Загрузить через OCR модель',
      uploadWithParser: 'Загрузить через парсер',
      uploadText: 'Загрузить текст',
      chooseFileFirst: 'Сначала выберите файл.',
      uploaded: 'Загружен {name}; document id {id}',
    },
    document: {
      recognized: 'Распознанный документ',
      downloadOriginal: 'Скачать оригинал',
    },
    errors: {
      searchFailed: 'Поиск не выполнен',
    },
  },
};

function getInitialLocale(): Locale {
  const savedLocale = localStorage.getItem(storageKey);
  if (savedLocale === 'en' || savedLocale === 'ru') {
    return savedLocale;
  }

  return navigator.language.toLowerCase().startsWith('ru') ? 'ru' : 'en';
}

export const i18n = createI18n({
  legacy: false,
  locale: getInitialLocale(),
  fallbackLocale: 'en',
  messages,
});

export function setLocale(locale: Locale) {
  i18n.global.locale.value = locale;
  localStorage.setItem(storageKey, locale);
}

