<template>
  <n-space vertical :size="20" align="center" class="mt-10">
    <div><span>Search By Tags</span></div>
    <div class="w-100">
      <n-input-group>
        <n-input v-model:value="imageTagRef" placeholder="eg:car,person,..." />
        <n-button type="primary" ghost @click="search(1)"> Search </n-button>
      </n-input-group>
    </div>
    <div><span>OR Search By Url</span></div>
    <div class="w-200">
      <n-input-group>
        <n-input
          v-model:value="imageUrlRef"
          placeholder="eg:https://bucket.s3.amazonaws.com/example.jpg"
        />
        <n-button type="primary" ghost @click="search(2)"> Search </n-button>
      </n-input-group>
    </div>
    <div><span>OR Search By Image</span></div>
    <div>
      <n-upload
        list-type="image-card"
        :max="1"
        :custom-request="processFile"
        @before-upload="beforeUpload"
      >
      </n-upload>
    </div>
    <n-button type="primary" ghost @click="searchImage"> Search </n-button>
    <div class="w-100">
      <n-space vertical :size="10" align="center" class="mt-10">
        <span>Result:</span>
        <div v-for="item in list" :key="item.url" class="mt-4 w-80">
          <p class="break-normal font-mono">tags: {{ item.tags }}</p>
          <p class="break-normal font-mono">s3_url: {{ item.url }}</p>
          <img :src="item.url" />
        </div>
      </n-space>
    </div>
  </n-space>
</template>

<script setup lang="ts">
import {
  NUpload,
  NInputGroup,
  NInput,
  NButton,
  NSpace,
  UploadCustomRequestOptions,
  UploadFileInfo,
} from "naive-ui";
import { ref } from "vue";
import request from "axios";

interface Model {
  tags?: string[];
  url?: string;
}

const choseFile = ref<File>();

const imageTagRef = ref<string>("");
const imageUrlRef = ref<string>("");
const list = ref<Model[]>([]);

console.log(list);

const search = (type: number) => {
  const data: Model = {};
  if (type === 1) {
    data.tags = imageTagRef.value.split(",");
    data.url = "";
  }
  if (type === 2) {
    data.tags = [];
    data.url = imageUrlRef.value;
  }
  request.post("api/search", data).then((res) => {
    list.value = res.data.data;
  });
};

const processFile = ({ file }: UploadCustomRequestOptions) => {
  choseFile.value = file.file as File;
};

const searchImage = () => {
  const formData = new FormData();
  formData.append("file", choseFile.value as File);
  request.post("api/search/file", formData).then((res) => {
    list.value = res.data.data;
  });
};

const beforeUpload = async (data: { file: UploadFileInfo; fileList: UploadFileInfo[] }) => {
  if (data.file.file?.type === "image/png" || data.file.file?.type === "image/jpeg") {
    return true;
  }
  alert("PNG、JPG、JPGE can only be uploaded");
  return false;
};
</script>

<style scoped></style>
