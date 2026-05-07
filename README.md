# 巴克納瓦 | Bakunawa
這是由 **CDD 團隊** 在Claude AI協助下自主開發的 Discord 機器人，能在特定關鍵詞被提及時自動從預先設定的詞庫中隨機回應。完全支援伺服器隔離，每個伺服器都有獨立的詞庫配置。

![Bakunawa](https://cdn.discordapp.com/attachments/1058755803198279794/1501947981262491760/Bakunawa__.png?ex=69fded8f&is=69fc9c0f&hm=e0bcdc7f8cbdace21567e79c977f91fcdbf8c8929a6341c3c374f8c2357a5ee2&)

## ✨ 主要特性

- 🎯 **自動觸發回應** - 偵測特定字串並隨機回應
- 🏘️ **伺服器隔離** - 每個伺服器的詞庫完全獨立，互不影響
- 📚 **多詞庫支援** - 內建「吃什麼」和「喝什麼」，支援自訂擴展
- ⚡ **動態管理** - 無需重啟即可添加/刪除回應
- 🌐 **雙語命令** - 支援英文和繁體中文命令別名
- 📝 **詳細幫助** - 內建幫助系統，新手友善
- 💾 **自動持久化** - 所有變更自動保存到 JSON 配置文件

## 🚀 快速開始

### 前置需求

- Python 3.8 或更高版本
- Discord 伺服器（用於測試）
- Discord Bot Token

### 安裝步驟

1. **複製本專案**
```bash
git clone https://github.com/yourusername/Bakunawa.git
cd Bakunawa
```

2. **安裝依賴套件**
```bash
pip install -r requirements.txt
```

3. **設定 Discord Bot Token**

複製 `.env.example` 為 `.env`：
```bash
cp .env.example .env
```

編輯 `.env` 文件，填入你的 Bot Token：
```
DISCORD_TOKEN=你的_DISCORD_BOT_TOKEN
```

4. **運行機器人**
```bash
python Bakunawa.py
```

看到以下訊息表示成功啟動：
```
✅ 機器人已登入為 Bakunawa#xxxx
📁 詞庫文件夾：/path/to/guild_libraries
```

## 📖 使用說明

### 自動回應（無需命令）

直接在 Discord 聊天中提及觸發詞，機器人會自動回應：

```
你：吃什麼
機器人：披薩

你：喝什麼
機器人：奶茶
```

### 命令列表

| 命令 | 別名 | 說明 |
|------|------|------|
| `e!add_response <詞庫> <內容>` | `e!添加回應` | 添加新回應 |
| `e!remove_response <詞庫> <內容>` | `e!移除回應` | 移除回應 |
| `e!list_responses <詞庫>` | `e!詞庫內容` | 查看詞庫內容 |
| `e!list_libraries` | `e!詞庫列表` | 查看所有詞庫 |
| `e!test_trigger <詞庫>` | `e!測試` | 測試隨機回應 |
| `e!reload_config` | `e!重新載入配置` | 重新載入配置 |
| `e!help_bot` | `e!指南` `e!幫助` | 查看幫助 |

### 命令範例

**添加新回應**
```
e!添加回應 吃 蛋餅
✅ 已添加到 '吃' 詞庫：蛋餅
```

**查看詞庫內容**
```
e!詞庫內容 吃

📋 吃 (第 1 頁)
1. 漢堡
2. 炸雞
3. 牛肉麵
...
```

**測試隨機回應**
```
e!測試 喝

🎲 喝 隨機回應
奶茶
```

## 🏗️ 專案結構

```
Bakunawa/
├── Bakunawa.py                 # 主程式
├── requirements.txt            # Python 依賴
├── .env.example               # 環境變數範本
├── .gitignore                 # Git 忽略清單
├── README.md                  # 本文件
└── guild_libraries/           # 伺服器詞庫文件夾（自動建立）
    ├── guild_123456789.json   # 伺服器 A 的詞庫
    ├── guild_987654321.json   # 伺服器 B 的詞庫
    └── ...
```

## 🔧 設定

### 詞庫結構

每個伺服器的詞庫存放在 `guild_libraries/guild_{伺服器ID}.json`：

```json
{
  "詞庫": {
    "吃": {
      "觸發詞": ["吃什麼", "吃啥", "吃哪個"],
      "回應": ["漢堡", "披薩", "牛肉麵", ...]
    },
    "喝": {
      "觸發詞": ["喝什麼", "喝啥"],
      "回應": ["奶茶", "咖啡", "果汁", ...]
    }
  }
}
```

### 添加新詞庫

**方法 1：使用命令**
```
e!添加回應 玩什麼 原神
```

**方法 2：手動編輯 JSON**
在 `guild_libraries/guild_XXXXXXXXXX.json` 中添加：
```json
"玩": {
  "觸發詞": ["玩什麼", "玩啥"],
  "回應": ["麥塊", "艾爾登法環"]
}
```

然後執行：
```
e!重新載入配置
```

## 🛡️ 伺服器隔離機制

每個 Discord 伺服器都有完全獨立的詞庫：

```
伺服器 A (ID: 835293572468154368)
└── guild_835293572468154368.json
    └── 吃什麼 → [漢堡, 披薩, 牛肉麵, ...]

伺服器 B (ID: 938472893847293847)
└── guild_938472893847293847.json
    └── 吃什麼 → [壽司, 拉麵, 天婦羅, ...]
```

- ✅ 伺服器 A 的用戶添加的詞庫不會影響伺服器 B
- ✅ 每個伺服器可自訂自己的觸發詞和回應
- ✅ 完全的數據隔離和隱私保護

## 🐛 常見問題

### Q: 機器人不回應？
**A:** 檢查以下項目：
- ✅ Bot Token 是否正確設置在 `.env`
- ✅ 是否在伺服器頻道而非私聊
- ✅ 觸發詞是否與詞庫中完全匹配
- ✅ 詞庫是否非空（使用 `e!詞庫內容` 查看）

### Q: 在伺服器間複製詞庫？
**A:** 複製相應的 JSON 文件：
```bash
cp guild_libraries/guild_源伺服器ID.json guild_libraries/guild_目標伺服器ID.json
```

### Q: 如何備份詞庫？
**A:** 備份整個 `guild_libraries` 文件夾：
```bash
cp -r guild_libraries guild_libraries_backup
```

### Q: 能否修改命令前綴？
**A:** 編輯 `Bakunawa.py` 第 12 行：
```python
bot = commands.Bot(command_prefix='你的前綴!', intents=intents)
```

## 📚 進階用法

### 自訂狀態訊息

編輯 `on_ready()` 函數：
```python
custom_status = discord.CustomActivity(
    name="你的自訂狀態"
)
await bot.change_presence(status=discord.Status.online, activity=custom_status)
```

### 添加新詞庫型別

1. 編輯 `DEFAULT_CONFIG`
2. 在 `"詞庫"` 中添加新條目：
```python
"新詞庫": {
    "觸發詞": ["觸發詞1", "觸發詞2"],
    "回應": ["回應1", "回應2"]
}
```

### 條件觸發

如果需要更複雜的觸發邏輯，可修改 `on_message()` 函數的觸發檢查。

## 🔐 安全性

- ⚠️ **不要分享 `.env` 文件** - 它包含敏感的 Bot Token
- ✅ 在 `.gitignore` 中已排除 `.env` 和詞庫文件夾
- ✅ 使用環境變數存儲敏感資訊
- ✅ 建議定期備份 `guild_libraries` 文件夾

### .gitignore 建議

```
.env
.env.local
__pycache__/
*.pyc
guild_libraries/
*.backup
```

## 📝 許可證

本專案採用 [MIT 許可證](LICENSE)。您可自由使用、修改和分發此代碼。

## 🤝 貢獻

歡迎提交 Issues 和 Pull Requests

### 貢獻指南
1. Fork 本專案
2. 建立特性分支
3. 提交變更
4. 推送到分支 
5. 開啟 Pull Request

## 📞 聯絡方式

- GitHub Issues: 回報 Bug 或功能請求
- Discord: @siegestor

## CDD 是誰？
- **Crossing Dead Development** (跨越死亡開發)，由 Discord 用戶 `@siegestor` 與他的苦命朋友們共同組成。
