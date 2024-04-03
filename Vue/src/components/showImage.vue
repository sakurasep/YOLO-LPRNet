<script>
import axios from 'axios'; // 导入Axios

export default {
  data() {
    return {
      imageUrl: null
    }
  },
  methods: {
    onFileChange(event) {
      const file = event.target.files[0];
      this.imageUrl = URL.createObjectURL(file);
      this.uploadImage(file);
    },
    async uploadImage(file) {
      try {
        const formData = new FormData();
        formData.append('image', file);

        // 使用Axios将图片上传到后端的Flask应用程序
        const response = await axios.post('http://127.0.0.1:5000/upload', formData);

        // 处理成功上传后的响应，例如打印响应内容
        console.log(response.data);
      } catch (error) {
        // 处理上传失败的情况，例如打印错误信息
        console.error(error);
      }
    }
  }
}
</script>

<template>
  <div class="container">
    <input type="file" @change="onFileChange">
  </div>
  <div v-if="imageUrl" class="image-container">
    <img :src="imageUrl" alt="Selected Image" class="image-preview">
  </div>
</template>

<style scoped>
.container {
  display: flex;
  justify-content: center;
}

.image-container {
  display: flex;
  justify-content: center;
  margin-top: 50px; /* 设置图片容器与上传按钮之间的距离 */
}

.image-preview {
  max-width: 100%; /* 图片最大宽度为容器宽度 */
  height: 500px; /* 高度自适应 */
}
</style>