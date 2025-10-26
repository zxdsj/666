# Windows-MCP Web Console / Windows-MCP 网页控制台

[English](#english) | [中文](#中文)

---

## English

### 📖 Overview

**Windows-MCP Web Console** is an interactive web interface designed to communicate with the Windows-MCP API server. It features a delightful mascot named "Bubble" (泡泡) and provides a user-friendly chat interface for seamless interaction with Windows automation tools.

### ✨ Features

- **🎨 Beautiful Chat Interface**: Modern, gradient-styled UI with smooth animations
- **⚡ Real-time Conversations**: Interact with Windows-MCP API in real-time
- **🎭 Bubble Mascot**: A cute, interactive mascot that:
  - Floats gently on the screen
  - Encourages you with motivational messages
  - Bounces playfully when you've been idle
  - Responds to clicks with random encouraging messages
- **💾 Context Preservation**: Maintains conversation history for multi-turn dialogues
- **⌨️ Keyboard Support**: Press Enter to send messages
- **🗑️ Clear Chat Function**: Easy button to clear conversation history
- **📱 Responsive Design**: Works on desktop and mobile devices
- **🔄 Auto-scroll**: Automatically scrolls to the latest message

### 🚀 Getting Started

#### Prerequisites

1. **Windows-MCP Server**: Ensure the Windows-MCP server is running
2. **Modern Web Browser**: Chrome, Firefox, Edge, or Safari

#### Installation & Usage

##### Method 1: Using console.py Proxy Server (Recommended - Solves CORS Issues)

1. **Start the Windows-MCP Server**:
    ```bash
    uv run main.py --transport sse --host localhost --port 8000
    ```

2. **Start the Proxy Server**:
    ```bash
    python console.py
    # Or with custom port:
    python console.py --port 18989
    ```

3. **Access the Web Console**:
    - Open your browser and visit: `http://localhost:18989/console`
    - The proxy server automatically:
      - Serves the console.html interface
      - Forwards requests to the MCP server (http://localhost:8000)
      - Handles CORS issues
      - Implements auto-retry (3 attempts, 10s intervals)

##### Method 2: Direct Access (May Have CORS Issues)

1. **Start the Windows-MCP Server**:
    ```bash
    uv run main.py --transport sse --host localhost --port 8000
    ```

2. **Open the Web Console**:
    - Simply open `console.html` in your web browser
    - Or serve it using a local web server:
        ```bash
        python -m http.server 8080
        # Then visit http://localhost:8080/console.html
        ```

3. **Start Chatting**:
    - Type your message in the input box
    - Press Enter or click the "发送" (Send) button
    - Wait for Bubble to respond!

### 🎯 Interactive Features

#### Bubble Mascot Behaviors

- **Idle Detection**: After 5 minutes of inactivity, Bubble will:
  - Show encouraging messages
  - Bounce around to remind you to take a break
  
- **Click Interaction**: Click on Bubble to receive random encouraging or weather-related messages

- **Visual Characteristics**:
  - Semi-transparent, jelly-like appearance
  - Rotating star on top that glows
  - Cute eyes and smile
  - Smooth floating animation

### ⚙️ Configuration

To modify the API endpoint, edit the `API_ENDPOINT` constant in `console.html`:

```javascript
const API_ENDPOINT = 'http://localhost:8000/messages';
```

### 📡 API Requirements

The console expects the Windows-MCP API to:
- Accept POST requests at `/messages`
- Receive JSON with conversation history:
  ```json
  {
      "messages": [
          {"role": "user", "content": "Your message"},
          {"role": "assistant", "content": "Response"}
      ]
  }
  ```
- Return JSON response with assistant's reply

### 🎨 Customization

The console is built with vanilla HTML, CSS, and JavaScript, making it easy to customize:
- **Colors**: Modify gradient colors in CSS variables
- **Mascot**: Adjust bubble appearance in `.bubble-body` styles
- **Messages**: Edit `encouragingMessages` and `weatherMessages` arrays in JavaScript
- **Animations**: Customize keyframe animations in CSS

### 🔧 Troubleshooting

**Problem**: "无法连接 Windows-MCP API 服务器" or CORS Errors

**Solutions**:
- **Recommended**: Use `console.py` proxy server to avoid CORS issues
  ```bash
  python console.py
  # Then visit http://localhost:18989/console
  ```
- Ensure Windows-MCP server is running on `localhost:8000`
- Check that the server is started with SSE transport:
  ```bash
  uv run main.py --transport sse --host localhost --port 8000
  ```
- The proxy server will automatically retry failed connections (3 times, 10s intervals)
- Check browser console and proxy server logs for detailed error messages

### 📄 License

This project follows the same license as Windows-MCP (MIT License).

---

## 中文

### 📖 简介

**Windows-MCP 网页控制台** 是一个交互式网页界面，用于与 Windows-MCP API 服务器通信。它配备了一个名为"泡泡"的可爱吉祥物，并提供友好的聊天界面与 Windows 自动化工具进行交互。

### ✨ 功能特性

- **🎨 美观的聊天界面**: 现代渐变风格 UI 配合流畅动画
- **⚡ 实时对话**: 与 Windows-MCP API 实时交互
- **🎭 泡泡吉祥物**: 一个可爱的交互吉祥物，它会：
  - 在屏幕上轻轻浮动
  - 用鼓励的话语激励你
  - 当你长时间未操作时会开心地跳动
  - 点击时会随机显示鼓励性的话语
- **💾 上下文保存**: 保留对话历史用于多轮对话
- **⌨️ 键盘支持**: 按 Enter 键发送消息
- **🗑️ 清除对话功能**: 一键清除对话历史
- **📱 响应式设计**: 在桌面和移动设备上均可使用
- **🔄 自动滚动**: 自动滚动到最新消息

### 🚀 快速开始

#### 前置条件

1. **Windows-MCP 服务器**: 确保 Windows-MCP 服务器正在运行
2. **现代网页浏览器**: Chrome、Firefox、Edge 或 Safari

#### 安装和使用

##### 方法一: 使用 console.py 代理服务器 (推荐 - 解决 CORS 问题)

1. **启动 Windows-MCP 服务器**:
    ```bash
    uv run main.py --transport sse --host localhost --port 8000
    ```

2. **启动代理服务器**:
    ```bash
    python console.py
    # 或使用自定义端口:
    python console.py --port 18989
    ```

3. **访问网页控制台**:
    - 打开浏览器访问: `http://localhost:18989/console`
    - 代理服务器会自动:
      - 提供 console.html 界面
      - 转发请求到 MCP 服务器 (http://localhost:8000)
      - 处理 CORS 跨域问题
      - 实现自动重试 (3次尝试,间隔10秒)

##### 方法二: 直接访问 (可能存在 CORS 问题)

1. **启动 Windows-MCP 服务器**:
    ```bash
    uv run main.py --transport sse --host localhost --port 8000
    ```

2. **打开网页控制台**:
    - 直接在浏览器中打开 `console.html`
    - 或使用本地 Web 服务器:
        ```bash
        python -m http.server 8080
        # 然后访问 http://localhost:8080/console.html
        ```

3. **开始聊天**:
    - 在输入框中输入你的消息
    - 按 Enter 键或点击"发送"按钮
    - 等待泡泡回复！

### 🎯 交互功能

#### 泡泡吉祥物行为

- **闲置检测**: 5 分钟未操作后，泡泡会：
  - 显示鼓励消息
  - 跳动提醒你休息一下
  
- **点击交互**: 点击泡泡会随机接收到鼓励性或天气相关的消息

- **视觉特点**:
  - 半透明、果冻般的外观
  - 顶部带有发光的旋转星星
  - 可爱的眼睛和笑容
  - 流畅的浮动动画

### ⚙️ 配置

要修改 API 端点，请编辑 `console.html` 中的 `API_ENDPOINT` 常量:

```javascript
const API_ENDPOINT = 'http://localhost:8000/messages';
```

### 📡 API 要求

控制台期望 Windows-MCP API:
- 在 `/messages` 接受 POST 请求
- 接收包含对话历史的 JSON:
  ```json
  {
      "messages": [
          {"role": "user", "content": "你的消息"},
          {"role": "assistant", "content": "回复"}
      ]
  }
  ```
- 返回包含助手回复的 JSON 响应

### 🎨 自定义

控制台使用纯 HTML、CSS 和 JavaScript 构建，易于自定义:
- **颜色**: 修改 CSS 中的渐变颜色
- **吉祥物**: 调整 `.bubble-body` 样式中的泡泡外观
- **消息**: 编辑 JavaScript 中的 `encouragingMessages` 和 `weatherMessages` 数组
- **动画**: 自定义 CSS 中的关键帧动画

### 🔧 故障排除

**问题**: "无法连接 Windows-MCP API 服务器" 或 CORS 跨域错误

**解决方法**:
- **推荐**: 使用 `console.py` 代理服务器避免 CORS 问题
  ```bash
  python console.py
  # 然后访问 http://localhost:18989/console
  ```
- 确保 Windows-MCP 服务器在 `localhost:8000` 上运行
- 检查服务器是否以 SSE 传输方式启动:
  ```bash
  uv run main.py --transport sse --host localhost --port 8000
  ```
- 代理服务器会自动重试失败的连接 (3次,间隔10秒)
- 检查浏览器控制台和代理服务器日志中的详细错误消息

### 📄 许可证

此项目遵循与 Windows-MCP 相同的许可证（MIT 许可证）。

---

## 📸 Screenshots / 截图

### Chat Interface / 聊天界面
- Beautiful gradient design with bubble messages
- 美丽的渐变设计和气泡消息

### Bubble Mascot / 泡泡吉祥物
- Cute, interactive mascot that floats and encourages
- 可爱的交互吉祥物，浮动和鼓励

---

## 🤝 Contributing / 贡献

Contributions are welcome! Feel free to submit issues and pull requests.

欢迎贡献！请随意提交问题和拉取请求。

## 🙏 Acknowledgments / 致谢

- Built for [Windows-MCP](https://github.com/CursorTouch/Windows-MCP)
- Designed with ❤️ for the Windows automation community

---

**Enjoy chatting with Bubble! / 享受与泡泡聊天的乐趣！** 🎉
