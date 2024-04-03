<template>
  <div class="container">
    <div class="content">
      <el-button type="primary" @click="fetchPredictedPlate">获取预测的车牌号码</el-button>
      <h2 class="plate">{{ predictedPlate }}</h2>
    </div>
  </div>
</template>

<script>
import {ref} from 'vue'; // 导入 ref 函数

export default {
  setup() {
    const predictedPlate = ref(''); // 定义响应式变量 predictedPlate

    const fetchPredictedPlate = () => {
      fetch('http://127.0.0.1:5000/predict_plate')
          .then(response => response.json())
          .then(data => {
            predictedPlate.value = data.plate; // 从后端返回的 JSON 数据中获取车牌号码
          })
          .catch(error => {
            console.error('获取预测车牌号码时出错：', error);
          });
    };

    return {
      predictedPlate,
      fetchPredictedPlate
    };
  }
};
</script>

<style scoped>
.container {
  display: flex;
  justify-content: center;
}

.content {
  text-align: center;
}

.title {
  margin-bottom: 20px; /* 标题与按钮之间的垂直间距 */
}

.plate {
  margin-bottom: 40px; /* 结果与按钮之间的垂直间距 */
}
</style>
