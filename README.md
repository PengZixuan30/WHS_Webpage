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

### 前端

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

### 后端

```bash
cd backend

# 创建 Python 虚拟环境
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

| 变量 | 浅色模式 | 深色模式 |
|------|----------|----------|
| `--bg-color` | `#fff8e7` | `#0b1d3a` |
| `--text-color` | `#333333` | `#f5f5f5` |
| `--links-color` | `#7c8b9e` | `#cbd5e1` |
| `--navbar-bg` | 奶油色半透明 | 深蓝半透明 |

手动切换通过 `<html>` 上的 `.dark` / `.light` 类控制，未手动设置时跟随系统偏好。
