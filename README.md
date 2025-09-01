## 项目目录结构

```
easytool/                    # 工具指令优化模块
├── README.md               # 本文档
├── assets/                 # 资源文件
│   ├── front.png          # 前端展示图
│   └── logo.png           # 项目logo
├── data_funcqa/           # FuncQA数据集
├── data_restbench/        # RestBench数据集
├── data_toolbench/        # ToolBench数据集
├── easytool/              # 核心代码模块
│   ├── funcQA.py          # FuncQA处理
│   ├── restbench.py       # RestBench处理
│   ├── toolbench.py       # ToolBench处理
│   └── util.py            # 工具函数
├── main.py                # 主程序入口
└── requirements.txt       # 依赖包列表
```

### 核心模块功能说明

#### 1. 主控制模块
- **main.py**: 程序入口，负责参数解析、任务路由和执行控制
- **data_process.py**: 数据预处理，自动下载和格式化数据集

#### 2. 任务处理模块
- **funcQA.py**: 功能问答任务处理，支持多跳和单跳推理
- **toolbench.py**: 工具基准测试，API选择和参数预测
- **restbench.py**: REST API基准测试，任务分解和路径规划
- **toolbench_retrieve.py**: 带检索的工具基准测试

#### 3. 工具支持模块
- **util.py**: 通用工具函数，文件操作、数据清理、进度管理

#### 4. 数据存储模块
- **data_funcqa/**: FuncQA数据集存储
- **data_toolbench/**: ToolBench数据集存储
- **data_restbench/**: RestBench数据集存储


   
## 概述

基于LLM的智能体通常使用工具文档来掌握来自不同来源的工具选择和使用，但这些文档可能格式不一致、冗余过长，并且缺乏指令演示。

EasyTool是一种简单而有效的方法，可以从工具文档中创建清晰、结构化和统一的指令，以改进基于LLM的智能体在使用工具方面的能力。

## 实验

### 先决条件

- 准备依赖包：`pip install -r requirements.txt`
- 数据构建：`python3 data_process.py`
  
在运行任何命令之前，请确保您已设置必要的API密钥。将 `""` 替换为您的实际密钥。
```bash
export OPENAI_API_KEY="your_openai_api_key_here"
export RAPIDAPI_KEY="your_rapidapi_key_here"
```
### ToolBench
您需要首先从以下链接获取工具执行代码（./data/toolenv/tools.）：[Google Drive](https://drive.google.com/drive/folders/1yBUQ732mPu-KclJnuQELEhtKakdXFc3J) 或 [清华云盘](https://cloud.tsinghua.edu.cn/f/c9e50625743b40bfbe10/)，然后将它们保存到 ./toolenv/tools
要使用LLM进行推理，请运行以下命令：
```bash
unzip data_toolbench/tool_instruction/API_description_embeddings.zip -d data_toolbench/tool_instruction/

export OPENAI_API_KEY=""
export RAPIDAPI_KEY=""

python3 main.py --model_name deepseek-chat --task toolbench --data_type G2 --tool_root_dir ./toolenv/tools

python3 main.py --model_name deepseek-chat --task toolbench --data_type G3 --tool_root_dir ./toolenv/tools

python3 main.py --model_name deepseek-chat --task toolbench_retrieve --data_type G2 --tool_root_dir ./toolenv/tools

python3 main.py --model_name deepseek-chat --task toolbench_retrieve --data_type G3 --tool_root_dir ./toolenv/tools
```

### FuncQA

要使用LLM进行推理，请运行以下命令：
```bash
export OPENAI_API_KEY=""

python3 main.py \
    --model_name gpt-3.5-turbo \
    --task funcqa \
    --data_type funcqa_mh

python3 main.py \
    --model_name deepseek-chat \
    --task funcqa \
    --data_type funcqa_oh
```

### 结果评估

#### FuncQA 评估脚本

项目提供了专门的评估脚本 `evaluate_funcQA.py` 来计算 FuncQA 任务的正确率和错误率。

**基本用法**：
```bash
# 评估 funcqa_mh 数据集结果
python evaluate_funcQA.py FuncQA_funcqa_mh_deepseek-chat_easytool.jsonl

# 评估 funcqa_oh 数据集结果
python evaluate_funcQA.py FuncQA_funcqa_oh_deepseek-chat_easytool.jsonl
```

**显示详细错误信息**：
```bash
python evaluate_funcQA.py results.jsonl --details
```

**生成 JSON 格式报告**：
```bash
python evaluate_funcQA.py results.jsonl --output report.json
```

**评估结果说明**：
- **总题数**：数据集中的问题总数
- **正确数**：check_index 为 1 的题目数量
- **错误数**：check_index 为 -1 的题目数量
- **正确率**：正确数 / 总题数 × 100%
- **错误率**：错误数 / 总题数 × 100%

**示例输出**：
```
📊 FuncQA 评估报告
==================
📁 文件: FuncQA_funcqa_mh_deepseek-chat_easytool.jsonl
📈 总题数: 62
✅ 正确数: 55
❌ 错误数: 7
🎯 正确率: 88.71%
💥 错误率: 11.29%
```

### RestBench

要使用LLM进行推理，请运行以下命令：
```bash
export OPENAI_API_KEY=""

python3 main.py --model_name deepseek-chat --task restbench 
```

## 引用

如果您发现这项工作对您的方法有用，可以按以下方式引用论文：

    @article{yuan2024easytool,
      title   = {EASYTOOL: Enhancing LLM-based Agents with Concise Tool Instruction}, 
      author  = {Siyu Yuan and Kaitao Song and Jiangjie Chen and Xu Tan and Yongliang Shen and Ren Kan and Dongsheng Li and Deqing Yang},
      journal = {arXiv preprint arXiv:2401.06201},
      year    = {2024}
    }

## 致谢

- [ChatGPT](https://platform.openai.com/)
- [Hugging Face](https://huggingface.co/)
- [ToolBench](https://github.com/OpenBMB/ToolBench)
- [RestBench](https://github.com/Yifan-Song793/RestGPT)
- [FuncQA](https://github.com/Ber666/ToolkenGPT)
