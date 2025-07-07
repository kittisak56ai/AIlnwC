# เปลี่ยนจาก feedparser เป็น atoma
import atoma
import requests
import discord
from discord.ext import commands, tasks
import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ฟังก์ชันสำหรับดึงข้อมูล RSS
def fetch_rss_feed(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        # ใช้ atoma แทน feedparser
        feed = atoma.parse_rss_bytes(response.content)
        return feed
    except Exception as e:
        print(f"Error fetching RSS feed: {e}")
        return None

# ฟังก์ชันแปลงข้อมูล feed จาก atoma ให้เหมือน feedparser
def convert_atoma_to_feedparser_format(feed):
    if not feed:
        return None
    
    # สร้าง object ที่มีรูปแบบคล้าย feedparser
    class FeedParserLike:
        def __init__(self, atoma_feed):
            self.entries = []
            for item in atoma_feed.items:
                entry = type('Entry', (), {})()
                entry.title = item.title
                entry.link = item.link
                entry.published = item.pub_date.isoformat() if item.pub_date else ""
                entry.summary = getattr(item, 'description', '') or ''
                self.entries.append(entry)
    
    return FeedParserLike(feed)

# ใช้ในโค้ดหลัก
# แทนที่ feedparser.parse(url) ด้วย:
# feed_data = fetch_rss_feed(url)
# feed = convert_atoma_to_feedparser_format(feed_data)

# ส่วนที่เหลือของโค้ดยังคงเหมือนเดิม...
