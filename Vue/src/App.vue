<template>
  <div class="app-container">
    <!-- 顶部标题栏 -->
    <el-header class="header">
      <h1 class="title">基于 YOLOv8 和 LPRNet 的车牌识别系统</h1>
    </el-header>

    <!-- 页面内容 -->
    <el-main class="main">
      <el-row>
        <!-- 左侧内容 -->
        <el-col :span="12" class="left-col">
          <ShowImage />
        </el-col>

        <!-- 右侧内容 -->
        <el-col :span="12" class="right-col">
          <ShowResult />
        </el-col>
      </el-row>
    </el-main>
  </div>
</template>

<script>
import ShowImage from "./components/showImage.vue";
import ShowResult from "./components/showResult.vue";

export default {
  components: {
    ShowImage,
    ShowResult
  }
}
</script>

<style scoped>
.app-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
}

.header {
  display: flex;
  justify-content: center; /* 水平居中对齐 */
  align-items: center; /* 垂直居中对齐 */
  background-color: #409EFF; /* 设置标题栏背景色 */
  color: #FFFFFF; /* 设置标题栏文字颜色 */
  padding: 20px; /* 上右下左 */
}

.title {
  font-size: 24px; /* 设置标题栏字体大小 */
}



.main {
  flex: 1; /* 设置内容区域自适应高度 */
}

.left-col, .right-col {
  padding: 20px; /* 设置左右内容区域的内边距 */
}
</style>
