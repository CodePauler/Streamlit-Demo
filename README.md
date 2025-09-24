https://app-demo-zhipu.streamlit.app/  

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/CodePauler/Streamlit-Demo)

**Streamlit** 是一个用 **Python** 快速构建交互式 Web 应用的开源框架，尤其适合数据分析、机器学习可视化和原型展示。它的特点是：

---

### ✅ **核心概念**

1. **简单易用**

   * 不需要掌握前端开发（HTML、CSS、JS），用纯 Python 代码就能生成网页界面。
   * 常用语法和 Jupyter Notebook 类似，降低了学习成本。

2. **快速构建交互**

   * 提供了丰富的小部件（Widgets），如按钮、滑块、文件上传、下拉选择框等。
   * 通过 `st.button`、`st.slider` 等 API，即可实现用户交互。

3. **实时刷新**

   * 当用户在界面上操作时，Streamlit 会自动重新运行 Python 脚本并更新页面，实现“所见即所得”。

4. **专为数据应用设计**

   * 内置支持 **Matplotlib**、**Plotly**、**Pandas DataFrame** 等数据可视化库。
   * 非常适合演示模型预测、仪表盘、数据探索等任务。

---

### 📌 **安装与基本用法**

```bash
pip install streamlit
```

创建 `app.py`：

```python
import streamlit as st

st.title("你好，Streamlit 👋")
name = st.text_input("请输入你的名字：")
if st.button("打招呼"):
    st.write(f"你好，{name}！欢迎使用 Streamlit 🎉")
```

运行：

```bash
streamlit run app.py
```

浏览器会打开一个本地网页，显示交互界面。

---

### 🧰 **典型应用场景**

* 机器学习模型 Demo（上传数据 → 模型预测 → 输出结果）
* 数据可视化仪表盘（类似轻量版 BI 工具）
* 快速搭建内部工具或原型
* NLP/LLM 项目的对话或知识问答界面

---

### 🆚 **和其他框架对比**

| 框架               | 特点                        |
| ---------------- | ------------------------- |
| **Streamlit**    | 面向数据科学和 ML，简单直观，适合快速原型    |
| **Dash**         | 功能更复杂，适合需要高度自定义的生产级仪表盘    |
| **Flask/Django** | 通用 Web 框架，灵活但需要自己写前端或集成模板 |

---

💡 **一句话总结**：

> **Streamlit = “用几行 Python 代码就能把数据分析脚本变成交互式网页”的工具，非常适合数据科学家和机器学习工程师快速展示成果。**
