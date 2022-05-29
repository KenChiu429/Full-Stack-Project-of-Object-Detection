<template>
  <n-space vertical :size="20" align="center" class="mt-10">
    <span>Select a Image</span>
    <div>
      <n-upload
        list-type="image-card"
        :max="1"
        :custom-request="processFile"
        @before-upload="beforeUpload"
      >
      </n-upload>
    </div>
    <n-button type="primary" ghost @click="upload"> Upload </n-button>
  </n-space>
</template>

<script setup lang="ts">
import { NUpload, NSpace, UploadCustomRequestOptions, NButton } from "naive-ui";
import type { UploadFileInfo } from "naive-ui";
import { ref } from "vue";
import request from "axios";

const choseFile = ref<File>();

const processFile = ({ file }: UploadCustomRequestOptions) => {
  choseFile.value = file.file as File;
};

const upload = () => {
  const formData = new FormData();
  formData.append("file", choseFile.value as File);
  request.post("api/image", formData).then((res) => {
    alert(res.data?.message);
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
