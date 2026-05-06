import discord
from discord.ext import commands
import random
import json
import os
from typing import Dict, List
from pathlib import Path

# 設定機器人
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='e!', intents=intents)

# 配置文件目錄
LIBRARIES_DIR = "guild_libraries"
DEFAULT_CONFIG = {
    "詞庫": {
        "吃": {
            "觸發詞": ["吃什麼", "吃啥", "吃哪個"],
            "回應": [
                "漢堡",
                "炸雞",
                "牛肉麵",
                "壽司",
                "披薩",
                "咖哩飯",
                "烤肉",
                "水餃",
                "炒飯",
                "火鍋",
                "便當",
                "湯麵",
                "自助餐",
                "麥當勞",
                "滷味",
                "沙拉清爽又健康",
                "肯德基",
                "義大利麵",
                "雞排",
                "DJ KHALED 雞翅", 
                "炸醬麵",
                "牛排",
                "泡麵",
                "生魚片",
                "壽司郎",
                "爭鮮",
                "迴轉壽司",
                "拉麵",
                "豬腳",
                "雞肉飯",
                "牛肉飯",
                "羊肉爐",
                "麻辣鍋",
                "素食餐",
                "生鮪魚蓋飯",
                "牛丼",
                "豬排",
                "雞排飯",
                "豬血糕",
                "麵包",
                "蛋餅",
                "牛奶鍋",
                "韓式料理",
                "越南河粉",
                "泰式料理",
                "印度咖哩",
                "薩利亞",
                "豆沙包",
                "延世大學生乳包",
                "稀飯",
                "吉野家",
                "摩斯漢堡",
                "漢堡王",
                "Sukiya",
                "Subway",
                "蔥肉餅",
                "蔥油餅",
                "鍋燒意麵",
                "不要吃"
            ]
        },
        "喝": {
            "觸發詞": ["喝什麼", "喝啥", "喝哪個"],
            "回應": [
                "奶茶",
                "果汁",
                "豆漿",
                "牛奶",
                "綠茶",
                "檸檬茶",
                "舒跑",
                "氣泡水",
                "蜂蜜水",
                "無糖茶",
                "養樂多",
                "咖啡",
                "熱巧克力",
                "可樂",
                "雪碧",
                "芬達",
                "紅茶",
                "烏龍茶",
                "紅茶拿鐵",
                "抹茶拿鐵",
                "珍珠奶茶",
                "多多綠",
                "古早味紅茶",
                "冬瓜茶",
                "冬瓜檸檬",
                "白開水",
                "熱水",
                "冰水",
                "椰子水",
                "葡萄汁",
                "柳橙汁",
                "蘋果汁",
                "西瓜汁",
                "不要喝"
            ]
        }
    }
}

# 確保目錄存在
Path(LIBRARIES_DIR).mkdir(exist_ok=True)


class LibraryManager:
    """管理詞庫的類（支持伺服器隔離）"""
    
    def __init__(self, guild_id: int):
        """
        初始化詞庫管理器
        每個伺服器有獨立的配置文件
        """
        self.guild_id = guild_id
        self.config_file = os.path.join(LIBRARIES_DIR, f"guild_{guild_id}.json")
        self.data = self.load()
    
    def load(self) -> dict:
        """從 JSON 文件載入詞庫"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️ 無法讀取配置文件 (Guild {self.guild_id}): {e}")
                return DEFAULT_CONFIG.copy()
        else:
            print(f"ℹ️ 伺服器 {self.guild_id} 的配置文件不存在，使用預設配置")
            return DEFAULT_CONFIG.copy()
    
    def save(self) -> bool:
        """保存詞庫到 JSON 文件"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"❌ 無法保存配置文件 (Guild {self.guild_id}): {e}")
            return False
    
    def get_libraries(self) -> dict:
        """獲取所有詞庫"""
        return self.data.get("詞庫", {})
    
    def add_response(self, library_type: str, response: str) -> bool:
        """添加新回應"""
        if library_type not in self.data["詞庫"]:
            return False
        
        if response not in self.data["詞庫"][library_type]["回應"]:
            self.data["詞庫"][library_type]["回應"].append(response)
            return self.save()
        return False
    
    def remove_response(self, library_type: str, response: str) -> bool:
        """移除回應"""
        if library_type not in self.data["詞庫"]:
            return False
        
        if response in self.data["詞庫"][library_type]["回應"]:
            self.data["詞庫"][library_type]["回應"].remove(response)
            return self.save()
        return False
    
    def get_random_response(self, library_type: str) -> str or None:
        """獲取隨機回應"""
        if library_type not in self.data["詞庫"]:
            return None
        
        responses = self.data["詞庫"][library_type]["回應"]
        return random.choice(responses) if responses else None


def get_library_manager(guild_id: int) -> LibraryManager:
    """
    獲取特定伺服器的詞庫管理器
    每個伺服器都有自己的實例
    """
    return LibraryManager(guild_id)

@bot.event
async def on_ready():
    custom_status = discord.CustomActivity(name="幫你決定吃什麼喝什麼，或是不要吃")
    await bot.change_presence(status=discord.Status.online, activity=custom_status)
    print(f"✅ 機器人已登入為 {bot.user}")
    print(f"📁 詞庫文件夾：{os.path.abspath(LIBRARIES_DIR)}")


@bot.event
async def on_message(message: discord.Message):
    # 忽略機器人自己的訊息
    if message.author == bot.user:
        return

    # 只在伺服器中處理（不處理私信）
    if message.guild is None:
        return

    user_message = message.content.strip()
    library_manager = get_library_manager(message.guild.id)
    libraries = library_manager.get_libraries()
    
    # 檢查是否觸發任何詞庫
    for library_type, library_data in libraries.items():
        triggers = library_data.get("觸發詞", [])
        for trigger in triggers:
            if trigger in user_message:
                response = library_manager.get_random_response(library_type)
                if response:
                    await message.reply(response)
                    return

    await bot.process_commands(message)


@bot.command(name='add_response', aliases=['添加回應'])
async def add_response(ctx, library_type: str, *, response: str):
    """添加新的回應到詞庫"""
    if ctx.guild is None:
        await ctx.send("❌ 此命令只能在伺服器中使用")
        return

    library_manager = get_library_manager(ctx.guild.id)
    
    if library_type not in library_manager.get_libraries():
        await ctx.send(f"❌ 找不到詞庫：{library_type}")
        return
    
    if library_manager.add_response(library_type, response):
        await ctx.send(f"✅ 已添加到 '{library_type}' 詞庫：{response}")
    else:
        await ctx.send(f"⚠️ 這個回應已經存在於 '{library_type}' 詞庫中")


@bot.command(name='remove_response', aliases=['移除回應'])
async def remove_response(ctx, library_type: str, *, response: str):
    """從詞庫中移除回應"""
    if ctx.guild is None:
        await ctx.send("❌ 此命令只能在伺服器中使用")
        return

    library_manager = get_library_manager(ctx.guild.id)
    
    if library_type not in library_manager.get_libraries():
        await ctx.send(f"❌ 找不到詞庫：{library_type}")
        return
    
    if library_manager.remove_response(library_type, response):
        await ctx.send(f"✅ 已從 '{library_type}' 詞庫移除：{response}")
    else:
        await ctx.send(f"❌ 在 '{library_type}' 詞庫中找不到：{response}")


@bot.command(name='list_responses', aliases=['詞庫內容'])
async def list_responses(ctx, library_type: str = None):
    """列出詞庫中的所有回應"""
    if ctx.guild is None:
        await ctx.send("❌ 此命令只能在伺服器中使用")
        return

    library_manager = get_library_manager(ctx.guild.id)
    libraries = library_manager.get_libraries()
    
    if library_type is None:
        # 列出所有詞庫
        embed = discord.Embed(title="📚 所有詞庫", color=discord.Color.blue())
        for lib_type, lib_data in libraries.items():
            triggers = ", ".join(lib_data.get("觸發詞", []))
            count = len(lib_data.get("回應", []))
            embed.add_field(
                name=lib_type,
                value=f"觸發詞：{triggers}\n項目數：{count}",
                inline=False
            )
        await ctx.send(embed=embed)
    elif library_type not in libraries:
        await ctx.send(f"❌ 找不到詞庫：{library_type}")
    else:
        lib_data = libraries[library_type]
        items = lib_data.get("回應", [])
        triggers = ", ".join(lib_data.get("觸發詞", []))
        
        if len(items) > 20:
            # 分頁顯示
            for i in range(0, len(items), 20):
                chunk = items[i:i+20]
                embed = discord.Embed(
                    title=f"📋 {library_type} (第 {i//20 + 1} 頁)",
                    description="\n".join(f"{idx+1}. {item}" for idx, item in enumerate(chunk)),
                    color=discord.Color.green()
                )
                embed.set_footer(text=f"觸發詞：{triggers}")
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title=f"📋 {library_type}",
                description="\n".join(f"{idx+1}. {item}" for idx, item in enumerate(items)),
                color=discord.Color.green()
            )
            embed.set_footer(text=f"觸發詞：{triggers}")
            await ctx.send(embed=embed)


@bot.command(name='list_libraries', aliases=['詞庫列表'])
async def list_libraries(ctx):
    """列出所有可用的詞庫"""
    if ctx.guild is None:
        await ctx.send("❌ 此命令只能在伺服器中使用")
        return

    library_manager = get_library_manager(ctx.guild.id)
    libraries = library_manager.get_libraries()
    
    if not libraries:
        await ctx.send("❌ 沒有可用的詞庫")
        return
    
    embed = discord.Embed(
        title="📚 可用的詞庫列表",
        color=discord.Color.blue()
    )
    
    for library_type in libraries.keys():
        embed.add_field(name=library_type, value=f"使用 `e!詞庫列表 {library_type}` 查看詳情", inline=False)
    
    await ctx.send(embed=embed)


@bot.command(name='test_trigger', aliases=['測試'])
async def test_trigger(ctx, library_type: str):
    """測試某個詞庫的觸發"""
    if ctx.guild is None:
        await ctx.send("❌ 此命令只能在伺服器中使用")
        return

    library_manager = get_library_manager(ctx.guild.id)
    response = library_manager.get_random_response(library_type)
    if response:
        embed = discord.Embed(
            title=f"🎲 {library_type} 隨機回應",
            description=response,
            color=discord.Color.yellow()
        )
        await ctx.send(embed=embed)
    else:
        await ctx.send(f"❌ 找不到詞庫或詞庫為空：{library_type}")


@bot.command(name='reload_config', aliases=['重新載入配置'])
async def reload_config(ctx):
    """重新載入配置文件（此命令已自動化，通常不需要手動執行）"""
    if ctx.guild is None:
        await ctx.send("❌ 此命令只能在伺服器中使用")
        return

    library_manager = get_library_manager(ctx.guild.id)
    library_manager.data = library_manager.load()
    libraries = library_manager.get_libraries()
    await ctx.send(f"✅ 配置已重新載入，共 {len(libraries)} 個詞庫")


@bot.command(name='help_bot', aliases=['指南', '幫助'])
async def help_bot(ctx):
    """顯示機器人指南"""
    embed = discord.Embed(
        title=" 巴克納瓦 | Bakunawa",
        description="使用說明",
        color=discord.Color.purple()
    )
    
    embed.add_field(
        name="📝 自動回應",
        value="在訊息中提及任何觸發詞，機器人會自動回應",
        inline=False
    )
    
    embed.add_field(
        name="📋 查詢命令",
        value="• `e!list_libraries` / `e!詞庫列表` - 查看所有詞庫\n"
              "• `e!list_responses <詞庫>` / `e!詞庫內容 <詞庫>` - 查看詞庫內容\n"
              "• `e!test_trigger <詞庫>` / `e!測試 <詞庫>` - 測試隨機回應",
        inline=False
    )
    
    embed.add_field(
        name="✏️ 編輯命令",
        value="• `e!add_response <詞庫> <回應>` / `e!添加回應 <詞庫> <回應>`\n"
              "• `e!remove_response <詞庫> <回應>` / `e!移除回應 <詞庫> <回應>`",
        inline=False
    )
    
    embed.add_field(
        name="⚙️ 管理命令",
        value="• `e!reload_config` / `e!重新載入配置` - 重新載入配置\n"
              "• `e!help_bot` / `e!指南` / `e!幫助` - 顯示此幫助",
        inline=False
    )
    
    embed.add_field(
        name="💡 提示",
        value="每個伺服器的詞庫是獨立的，不會與其他伺服器互通",
        inline=False
    )
    
    await ctx.send(embed=embed)


if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')
    
    if not TOKEN:
        print("❌ 錯誤：DISCORD_TOKEN 環境變數未設置")
        print("請在 .env 文件中設置 DISCORD_TOKEN")
        exit(1)
    
    bot.run(TOKEN)