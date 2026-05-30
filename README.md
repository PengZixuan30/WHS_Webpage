# WHS Webpage

望海服务器（WangHai Server）官方网站，支持中英文双语切换与深色/浅色主题。

## 项目架构

```
WHS_Webpage/
├── whs/                  # 前端 — Vue 3 + Vite
│   ├── public/                # 静态资源（直接映射到根路径）
│   │   └── icons.png
│   ├── src/
│   │   ├── App.vue            # 根组件（全局标题管理）
│   │   ├── main.js            # 入口，挂载 router / i18n
│   │   ├── style.css          # 全局样式 & CSS 变量（主题色）
│   │   ├── assets/            # 需构建处理的资源（图片等）
│   │   ├── components/        # 可复用组件
│   │   │   ├── top_navbar.vue     # 顶部导航栏
│   │   │   └── bottom_navbar.vue  # 底部导航栏（语言/主题切换）
│   │   ├── composables/       # 组合式函数
│   │   │   └── useLanguage.js     # 语言切换逻辑（localStorage 持久化）
│   │   ├── i18n/              # 国际化配置
│   │   │   └── index.js           # vue-i18n 初始化 & 浏览器语言检测
│   │   ├── locales/           # 翻译文件
│   │   │   ├── zh.json            # 中文
│   │   │   └── en.json            # 英文
│   │   ├── pages/             # 页面组件
│   │   │   └── home.vue           # 首页
│   │   └── router/            # 路由配置
│   │       └── index.js
│   ├── index.html             # HTML 入口
│   ├── vite.config.js         # Vite 配置
│   └── package.json           # 依赖 & 脚本
├── backend/                   # 后端 — FastAPI (Python)
│   └── main.py
└── README.md
```

## 技术栈

| 层级 | 技术 |
|------|------|
| 前端框架 | Vue 3 (Composition API + `<script setup>`) |
| 构建工具 | Vite |
| 路由 | Vue Router 5 |
| 国际化 | vue-i18n 9 |
| 图标 | lucide-vue-next |
| 后端框架 | FastAPI (Python) |

## 功能特性

- 🌐 **中英文双语切换** — 浏览器语言自动检测，手动选择后 localStorage 持久化
- 🌓 **深色/浅色主题切换** — 支持手动切换，兼容系统 `prefers-color-scheme`
- 📱 **响应式布局** — 适配桌面端与移动端（≤768px）
- 🔗 **路由标题联动** — 页面标题随路由和语言自动更新

## 快速启动

### 🚀 一键启动（推荐）

项目提供了启动脚本，可自动开启前后端服务：

| 平台 | 文件 | 使用方式 |
|------|------|----------|
| 跨平台 | `main.py` | `python main.py`（Windows）或 `python3 main.py`（macOS/Linux） |
| Windows | `start.bat` | 双击运行，或在终端执行 `.\start.bat` |
| macOS / Linux | `start.sh` | 先赋予执行权限：`chmod +x start.sh`，然后 `./start.sh` |

> [!NOTE]
> **推荐 `main.py`**：跨平台通用，前后端日志合并输出到同一终端，前缀 `[Backend]` / `[Frontend]` 区分来源，`Ctrl+C` 一键停止。

脚本会自动完成以下工作：

1. 激活 Python 虚拟环境 → 在 **8000** 端口启动 FastAPI 后端
2. 安装 npm 依赖 → 在 **5173** 端口启动 Vite 前端

> [!NOTE]
> **注意**：首次启动前请确保已安装 [Node.js](https://nodejs.org/) 和 [Python 3](https://www.python.org/)，且后端已创建虚拟环境（Windows 项目已预置 `backend/venv/`）。

---

### 手动启动

如果自动脚本无法使用，可按以下步骤手动启动各服务：

#### 前端

```bash
cd whs

# 安装依赖
npm install

# 启动开发服务器（默认 http://localhost:5173）
npm run dev

# 构建生产版本
npm run build

# 预览生产构建
npm run preview
```

#### 后端

```bash
cd backend

# 创建 Python 虚拟环境（仅首次）
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# macOS / Linux:
source venv/bin/activate

# 安装依赖
pip install fastapi uvicorn

# 启动开发服务器（默认 http://localhost:8000）
uvicorn main:app --reload
```

## CSS 变量（主题系统）

主题通过 CSS 自定义属性实现，定义在 `src/style.css`：

| 变量 | 用途 | 浅色模式 | 深色模式 |
|------|------|----------|----------|
| `--bg-color` | 页面背景色 | `#fff8e7` 奶油白 | `#0b1d3a` 深海蓝 |
| `--card-color` | 卡片/容器背景色 | `#ffffff` 纯白 | `#162d4a` 深蓝 |
| `--text-color` | 正文文字颜色 | `#333333` 深灰 | `#f5f5f5` 近白 |
| `--links-color` | 链接/次要文字颜色 | `#7c8b9e` 灰蓝 | `#cbd5e1` 浅灰蓝 |
| `--navbar-bg` | 导航栏背景（半透明） | `rgba(255,248,231,0.7)` | `rgba(11,29,58,0.7)` |
| `--notice-color` | 公告/提示背景（半透明） | `rgba(235,170,40,0.7)` 琥珀 | `rgba(240,184,96,0.7)` 浅琥珀 |

> 每个颜色变量均配有对应的 `-rgb` 版本（如 `--bg-color-rgb`），便于在 `rgba()` 中组合透明度使用。

手动切换通过 `<html>` 上的 `.dark` / `.light` 类控制，未手动设置时跟随系统偏好。
