<script setup lang="ts">
import Button from 'primevue/button';
import FileUpload, { type FileUploadSelectEvent } from 'primevue/fileupload';
import RadioButton from 'primevue/radiobutton';
import Tab from 'primevue/tab';
import TabList from 'primevue/tablist';
import TabPanel from 'primevue/tabpanel';
import TabPanels from 'primevue/tabpanels';
import Tabs from 'primevue/tabs';
import { ref } from 'vue';

import { uploadDocument, type ProcessingStrategy } from '../services/api';

const selectedFile = ref<File | null>(null);
const strategy = ref<ProcessingStrategy>('scanner_ocr');
const status = ref('');

function onSelect(event: FileUploadSelectEvent) {
  selectedFile.value = event.files[0] ?? null;
}

async function upload(strategyOverride?: ProcessingStrategy) {
  if (!selectedFile.value) {
    status.value = 'Choose a file first.';
    return;
  }

  const selectedStrategy = strategyOverride ?? strategy.value;
  const response = await uploadDocument(selectedFile.value, selectedStrategy);
  status.value = `Uploaded ${selectedFile.value.name}; document id ${response.document_id}`;
}
</script>

<template>
  <main class="upload-page">
    <h1>Upload Documents</h1>

    <Tabs value="pdf">
      <TabList>
        <Tab value="pdf">PDF/PBF</Tab>
        <Tab value="images">Images</Tab>
        <Tab value="office">Office</Tab>
        <Tab value="text">Text/Markdown</Tab>
      </TabList>

      <TabPanels>
        <TabPanel value="pdf">
          <div class="upload-panel">
            <FileUpload mode="basic" custom-upload choose-label="Choose PDF/PBF" @select="onSelect" />
            <label class="radio-row">
              <RadioButton v-model="strategy" input-id="scanner" value="scanner_ocr" />
              <span>Top scanner OCR</span>
            </label>
            <label class="radio-row">
              <RadioButton v-model="strategy" input-id="ocr-model" value="ocr_model" />
              <span>OCR model via OpenAI API</span>
            </label>
            <Button label="Upload" @click="upload()" />
          </div>
        </TabPanel>

        <TabPanel value="images">
          <div class="upload-panel">
            <FileUpload mode="basic" custom-upload choose-label="Choose image" @select="onSelect" />
            <Button label="Upload with OCR model" @click="upload('ocr_model')" />
          </div>
        </TabPanel>

        <TabPanel value="office">
          <div class="upload-panel">
            <FileUpload mode="basic" custom-upload choose-label="Choose office file" @select="onSelect" />
            <Button label="Upload with parser" @click="upload('parser')" />
          </div>
        </TabPanel>

        <TabPanel value="text">
          <div class="upload-panel">
            <FileUpload mode="basic" custom-upload choose-label="Choose text/Markdown" @select="onSelect" />
            <Button label="Upload text" @click="upload('parser')" />
          </div>
        </TabPanel>
      </TabPanels>
    </Tabs>

    <p v-if="status" class="upload-status">{{ status }}</p>
  </main>
</template>

