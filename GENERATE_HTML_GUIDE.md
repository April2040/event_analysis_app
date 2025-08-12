# 🎨 高级HTML生成器 - 使用指南

## 📝 **简单说明**

`generate_advanced_html.py` 是一个**独立的工具**，用于将分析的TXT文件转换为高级可视化HTML页面。

## 🚀 **使用方法**

### **方法1: 自动处理（最简单）**
```bash
# 直接运行，自动处理最新的分析文件
python3 generate_advanced_html.py
```

**说明：**
- ✅ 不需要你手动指定文件
- ✅ 自动找到 temp/ 文件夹中最新的分析文件
- ✅ 自动生成高级HTML版本

### **方法2: 指定文件**
```bash
# 处理特定的分析文件
python3 generate_advanced_html.py temp/temp_analysis_20250812_093043.txt
```

## 📋 **完整工作流程示例**

### **场景1: 日常使用**
1. 在网页 http://localhost:8002 进行分析（勾选快速模式）
2. 分析完成后，运行：
   ```bash
   python3 generate_advanced_html.py
   ```
3. 在浏览器中打开生成的HTML文件

### **场景2: 历史文件转换**
如果你有之前的分析文件想要转换：
```bash
# 查看所有分析文件
ls temp/temp_analysis_*.txt

# 选择想要转换的文件
python3 generate_advanced_html.py temp/temp_analysis_20250812_092929.txt
```

## 📁 **文件结构说明**

转换前后的文件对应关系：
```
输入文件: temp/temp_analysis_20250812_093043.txt
输出文件: temp/temp_analysis_20250812_093043_advanced.html
```

## 🌐 **如何查看结果**

生成完成后，工具会显示：
```
✅ 高级HTML生成成功: temp/temp_analysis_20250812_093043_advanced.html
🌐 可在浏览器打开: file:///Users/qiyi/coding/event_analysis_app/temp/temp_analysis_20250812_093043_advanced.html
```

**打开方式：**
1. 复制显示的文件路径到浏览器地址栏
2. 或者直接双击HTML文件
3. 或者右键选择"用浏览器打开"

## ❓ **常见问题**

**Q: 我需要手动导入TXT文件吗？**
A: 不需要！工具会自动读取TXT文件内容。

**Q: 如果没有分析文件怎么办？**
A: 先在网页进行一次分析，生成TXT文件后再使用此工具。

**Q: 生成的HTML文件在哪里？**
A: 在 temp/ 文件夹中，文件名会添加 "_advanced.html" 后缀。

**Q: 可以删除原来的TXT文件吗？**
A: 建议保留，因为HTML是基于TXT生成的。

## 🎯 **推荐使用方式**

**最简单的方式：**
```bash
# 1. 完成网页分析后
# 2. 直接运行
python3 generate_advanced_html.py
# 3. 打开生成的HTML文件查看高级可视化效果
```

就这么简单！🎉
