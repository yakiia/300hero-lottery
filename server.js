const express = require("express");
const fs = require("fs");
const path = require("path");
const app = express();
const PORT = process.env.PORT || 3000;

// 允许跨域请求
app.use((req, res, next) => {
  res.setHeader("Access-Control-Allow-Origin", "*");
  next();
});

// 关键：让服务器提供对local_page_files文件夹的访问
app.use(
  "/local_page_files",
  express.static(path.join(__dirname, "local_page_files"))
);

// 提供public文件夹中的前端文件
app.use(express.static(path.join(__dirname, "public")));

// 读取英雄数据
let heroesData = [];
const heroesPath = path.join(__dirname, "heroes.json");

try {
  const data = fs.readFileSync(heroesPath, "utf8");
  heroesData = JSON.parse(data);
  console.log(`已加载 ${heroesData.length} 个英雄数据`);
} catch (err) {
  console.error("读取英雄数据失败:", err.message);
}

// 随机英雄API
app.get("/api/random/:count", (req, res) => {
  try {
    const count = parseInt(req.params.count);
    if (isNaN(count) || count < 1 || count > 10) {
      return res.status(400).json({ error: "请提供1-10之间的数字" });
    }

    if (heroesData.length < count) {
      return res
        .status(400)
        .json({ error: `英雄数量不足（当前${heroesData.length}个）` });
    }

    // 随机选择英雄
    const shuffled = [...heroesData].sort(() => 0.5 - Math.random());
    res.json(shuffled.slice(0, count));
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// 获取全部英雄
app.get("/api/all", (req, res) => {
  res.json(heroesData);
});

app.listen(PORT, "0.0.0.0", () => {
  console.log(`Server ready on port ${PORT}`);
});
