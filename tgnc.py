"""
╔══════════════════════════════════════════════════════════════════════╗
║                 ⚡ HYPER-X BOT SCRIPT v3.0 (ULTIMATE) ⚡             ║
║                  WITH TECH-X FUSION ENGINE & PRELOADER               ║
╠══════════════════════════════════════════════════════════════════════╣
║  [REQUIRED PACKAGES]                                                 ║
║  >>> pip install python-telegram-bot httpx pillow gTTS               ║
╚══════════════════════════════════════════════════════════════════════╝
"""

import asyncio
import os
import sys
import io
import time
import logging
import random
import re
import signal
from collections import deque
from datetime import datetime
from typing import Dict, Set, List, Optional

from telegram import Update, ReactionTypeEmoji
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.constants import ChatType
from telegram.error import RetryAfter, TimedOut, NetworkError, BadRequest, Forbidden

logging.basicConfig(
    format="%(asctime)s - [HYPER] - %(levelname)s - %(message)s",
    level=logging.WARNING
)
logger = logging.getLogger("HyperBot")

OWNER_ID = 5206554804
DEFAULT_AUTHORIZED_USERS = {5961069280}
HYPER_MODE = True

# 22 BOT TOKENS INTEGRATED
BOT_TOKENS = [
    "8715370740:AAFBnlui03ZnF6ILK6q1takgdQPJNM5_kpU",
    "8582315119:AAH7oL74paJfIzPPX80xjX0qtIu5bjQNWH8",
    "8256576860:AAGz4v1NBlftdY5n-7s2wrlDhuPKvA1-J9g",
    "8076553437:AAFFnZ5rkNPRTcJjOPhY0gN9erjbIdvPtnI",
    "8546834207:AAFNaDnMOdlT6xW2Did-zRMvPWfKHEF2e-4",
    "8571782559:AAH6TH796Lcr0VuJwNW5eBlZhysP64SdBPQ",
    "8475642506:AAGgq73lcSeJv566HSNYuGOQZYEc52yLtJA",
    "8290089670:AAEsQYVsaRp6ePD0sN6DHWauQQvsCrkQX5o",
    "8383005233:AAH2arrnWTpseSnU0OAP0E1u-epY2YSoprg",
    "8542017249:AAFthHS4wkRt_yyPcHGbQzSf7ypoRllu7Qw",
    "7689093635:AAH4XvdjRmJAu2zH_jY8sDE4Rn4ML0DZSP4",
    "8244193403:AAEgcOvkWcEpvnnchC5ItoTb6SBXPvuYj-A",
    "8492426300:AAHFDja6CJ4aSzVRcFNx1bLyovDw5q0BDDQ",
    "8445634975:AAGOJNLhanSNClvAqcaesSpRGTex-NZ4m1M",
    "8317361651:AAEdiHVMJSBTUzhg_NzM-VT07MZFLItE74I",
    "8262328439:AAFEYYU8t4Xg9nk1N2XRq1XCMjpwCAAzXTM",
    "8368146897:AAFBRhZsC63F65dKZzFf5a_-Np2GH8GwxZ4",
    "7823733614:AAFnmv2BP_AdLeCy39tpbEYpaGJQO05CicE",
    "7595465023:AAEXaR4Au7iY7kpzGcVx7HKQcNmOzSGnkV4",
    "8088855553:AAHx84obLmj1JBHGMefEA8gFfib3f-V7v-s",
    "8176270936:AAFakNDas10mURG3AYSIYDVoT0klN0KNiIE",
    "8643321780:AAHmRTMb25jBPq6bEyNs0wxz1mwxAeQG4Cw"
]

HEART_EMOJIS = ['❤️', '🧡', '💛', '💚', '💙', '💜', '🤎', '🖤', '🤍', '💘', '💝', '💖', '💗', '💓', '💞', '💌', '💕', '💟', '♥️', '❣️', '💔']
VALID_REACTIONS = ["👎", "💩", "🤮", "🤡", "👺"]

GODSPEED_NAMES = [
    "⚡𝑇𝑀𝐾𝐶⚡", "🔥𝑅𝐴𝑁𝐷𝐼𝐾𝐸 𝑃𝐼𝐿𝐿𝐸🔥", "💀𝐷𝐸𝑉 𝐵𝐻𝐴𝐺𝑊𝐴𝑁 𝐾𝑂 𝐵𝐴𝐴𝑃 𝐵𝑁𝐴𝐴 𝐿𝐸💀", "👑𝑇𝐵𝐾𝐶👑", "✨𝑀𝐴𝐴 𝐶𝐻𝑈𝐷𝐴𝐴✨",
    "💥𝑇𝐸𝑅𝐼 𝑀𝐴𝐴 𝐾𝑂 𝐶𝐻𝑂𝐷𝑈💥", "❄️𝐶𝐻𝑈𝐷 𝑀𝐴𝐷𝐴𝑅𝐶𝐻𝑂𝐷❄️", "🌪️𝑅𝑁𝐷𝐼𝐾𝐸 𝑃𝐼𝐿𝐿𝐸🌪️", "🎯𝐵𝐻𝐸𝑁 𝐾𝑂 𝐶𝐻𝑂𝐷𝑈 𝑇𝐸𝑅𝐼 🎯", "🚀𝑀𝐴𝐴 𝐶𝐻𝑈𝐷𝐴 🚀"
]

NAME_CHANGE_MESSAGES = [
    "DEV TERA BAAP  🔥⃤⃟⃝🐦‍🔥『🚩』",
    "{target} TERI BHEN KA BHOSADA 🔥⃤⃟⃝🐦‍🔥『🚩』",
    "{target} TERI MAA DEV KE LUND PR 🔥⃤⃟⃝🐦‍🔥『🚩』",
    "{target} TERI MAA KA BHOSADA CHUDA 🔥⃤⃟⃝🐦‍🔥『🚩』",
    "{target} TERI CHUDAYI BY DEV PAPA 🔥⃤⃟⃝🐦‍🔥『🚩』",
    "{target} CVR LE RANDI KE BACCHE 🔥⃤⃟⃝🐦‍🔥『🚩』",
    "{target} TERI MAA RANDI 🔥⃤⃟⃝🐦‍🔥 『🚩』",
    "{target} TERI BHEN KAALI CHUT 🔥⃤⃟⃝🐦‍🔥『🚩』",
]

REPLY_MESSAGES = [
    "{target} ---RDI🐣",
    "{target} चुद गया -!",
    "Aʟᴏᴏ Kʜᴀᴋᴇ {target} Kɪ Mᴀ Cʜᴏᴅ Dᴜɴɢᴀ!",
    "{target} Cʜᴜᴅᴀ🦖🪽",
    "{target} Bᴏʟᴇ ᴅᴇᴠ ᴘᴀᴘᴀ पिताश्री Mᴇʀɪ Mᴀ Cʜᴏᴅ Dᴏ",
    "{target} Kɪ Mᴀ Bᴏʟᴇ ᴅᴇᴠ ᴘᴀᴘᴀ Sᴇ Cʜᴜᴅᴜɴɢɪ",
    "{target} Kɪ Bᴇʜɴ Kɪ Cʜᴜᴛ Kᴀʟɪ Kᴀʟɪ",
    "{target} Kɪ Mᴀ Rᴀɴᴅɪ",
    "{target} ɢᴀʀᴇᴇʙ ᴋᴀ ʙᴀᴄʜʜᴀ",
    "{target} ᴄʜᴜᴅ ᴋᴇ ᴘᴀɢᴀʟ ʜᴏɢᴀʏᴀ",
    "{target} ᴋɪ ʙᴇʜɴ ᴄʜᴏᴅᴜ",
    "{target} ʟᴜɴᴅ ᴄʜᴜsᴇɢᴀ sᴀʙᴋᴀ",
    "{target} ᴋɪ ᴍᴀ ᴋᴏ ᴄʜᴏᴅᴇ ᴅᴇᴠ ᴘᴀᴘᴀ",
    "{target} ᴋɪ ᴍᴀ ᴅᴇᴠ ᴘᴀᴘᴀ ꜱᴇ ᴄʜᴜᴅᴇ",
    "{target} ᴅᴇᴠ ᴘᴀᴘᴀ ꜱᴇ ᴄʜᴜᴅᴀ",
]

SPAM_MESSAGES = [
    """✝ 𝐀ɴᴛᴀ𝐑 𝐌ᴀɴ𝐓ᴀʀ 𝐒ʜᴀɪ𝐓ᴀɴ𝐈 𝐊ʜᴏ𝐏ᴀᴅ𝐀 {target} 𝐆ᴀ𝐑ɪ𝐁 𝐊ɪ 𝐀ᴍᴍ𝐈 𝐊ᴀ 𝐊ᴀʟ𝐀 𝐁ʜᴏs𝐃ᴀ  ━━━━━━━━ 💗᪲᪲᪲࣪ ִֶָ☾.ᯓᡣ𐭩🤍ྀི    ✝ 𝐀ɴᴛᴀ𝐑 𝐌ᴀɴ𝐓ᴀʀ 𝐒ʜᴀɪ𝐓ᴀɴ𝐈 𝐊ʜᴏ𝐏ᴀᴅ𝐀 {target} 𝐆ᴀ𝐑ɪ𝐁 𝐊ɪ 𝐀ᴍᴍ𝐈 𝐊ᴀ 𝐊ᴀʟ𝐀 𝐁ʜᴏs𝐃ᴀ  ━━━━━━━━ 💗᪲᪲᪲࣪ ִֶָ☾.ᯓᡣ𐭩🤍ྀི    ✝ 𝐀ɴᴛᴀ𝐑 𝐌ᴀɴ𝐓ᴀʀ 𝐒ʜᴀɪ𝐓ᴀɴ𝐈 𝐊ʜᴏ𝐏ᴀᴅ𝐀 {target} 𝐆ᴀ𝐑ɪ𝐁 𝐊ɪ 𝐀ᴍᴍ𝐈 𝐊ᴀ 𝐊ᴀʟ𝐀 𝐁ʜᴏs𝐃ᴀ  ━━━━━━━━ 💗᪲᪲᪲࣪ ִֶָ☾.ᯓᡣ𐭩🤍ྀི    ✝ 𝐀ɴᴛᴀ𝐑 𝐌ᴀɴ𝐓ᴀʀ 𝐒ʜᴀɪ𝐓ᴀɴ𝐈 𝐊ʜᴏ𝐏ᴀᴅ𝐀 {target} 𝐆ᴀ𝐑ɪ𝐁 𝐊ɪ 𝐀ᴍᴍ𝐈 𝐊ᴀ 𝐊ᴀʟ𝐀 𝐁ʜᴏs𝐃ᴀ  ━━━━━━━━ 💗᪲᪲᪲࣪ ִֶָ☾.ᯓᡣ𐭩🤍ྀི    ✝ 𝐀ɴᴛᴀ𝐑 𝐌ᴀɴ𝐓ᴀʀ 𝐒ʜᴀɪ𝐓ᴀɴ𝐈 𝐊ʜᴏ𝐏ᴀᴅ𝐀 {target} 𝐆ᴀ𝐑ɪ𝐁 𝐊ɪ 𝐀ᴍᴍ𝐈 𝐊ᴀ 𝐊ᴀʟ𝐀 𝐁ʜᴏs𝐃ᴀ  ━━━━━━━━ 💗᪲᪲᪲࣪ ִֶָ☾.ᯓᡣ𐭩🤍ྀི    ✝ 𝐀ɴᴛᴀ𝐑 𝐌ᴀɴ𝐓ᴀʀ 𝐒ʜᴀɪ𝐓ᴀɴ𝐈 𝐊ʜᴏ𝐏ᴀᴅ𝐀 {target} 𝐆ᴀ𝐑ɪ𝐁 𝐊ɪ 𝐀ᴍᴍ𝐈 𝐊ᴀ 𝐊ᴀʟ𝐀 𝐁ʜᴏs𝐃ᴀ  ━━━━━━━━ 💗᪲᪲᪲࣪ ִֶָ☾.ᯓᡣ𐭩🤍ྀི    ✝ 𝐀ɴᴛᴀ𝐑 𝐌ᴀɴ𝐓ᴀʀ 𝐒ʜᴀɪ𝐓ᴀɴ𝐈 𝐊ʜᴏ𝐏ᴀᴅ𝐀 {target} 𝐆ᴀ𝐑ɪ𝐁 𝐊ɪ 𝐀ᴍᴍ𝐈 𝐊ᴀ 𝐊ᴀʟ𝐀 𝐁ʜᴏs𝐃ᴀ  ━━━━━━━━ 💗᪲᪲᪲࣪ ִֶָ☾.ᯓᡣ𐭩🤍ྀི    ✝ 𝐀ɴᴛᴀ𝐑 𝐌ᴀɴ𝐓ᴀʀ 𝐒ʜᴀɪ𝐓ᴀɴ𝐈 𝐊ʜᴏ𝐏ᴀᴅ𝐀 {target} 𝐆ᴀ𝐑ɪ𝐁 𝐊ɪ 𝐀ᴍᴍ𝐈 𝐊ᴀ 𝐊ᴀʟ𝐀 𝐁ʜᴏs𝐃ᴀ  ━━━━━━━━ 💗᪲᪲᪲࣪ ִֶָ☾.ᯓᡣ𐭩🤍ྀི    ✝ 𝐀ɴᴛᴀ𝐑 𝐌ᴀɴ𝐓ᴀʀ 𝐒ʜᴀɪ𝐓ᴀɴ𝐈 𝐊ʜᴏ𝐏ᴀᴅ𝐀 {target} 𝐆ᴀ𝐑ɪ𝐁 𝐊ɪ 𝐀ᴍᴍ𝐈 𝐊ᴀ 𝐊ᴀʟ𝐀 𝐁ʜᴏs𝐃ᴀ  ━━━━━━━━ 💗᪲᪲᪲࣪ ִֶָ☾.ᯓᡣ𐭩🤍ྀི    ✝ 𝐀ɴᴛᴀ𝐑 𝐌ᴀɴ𝐓ᴀʀ 𝐒ʜᴀɪ𝐓ᴀɴ𝐈 𝐊ʜᴏ𝐏ᴀᴅ𝐀 {target} 𝐆ᴀ𝐑ɪ𝐁 𝐊ɪ 𝐀ᴍᴍ𝐈 𝐊ᴀ 𝐊ᴀʟ𝐀 𝐁ʜᴏs𝐃ᴀ  ━━━━━━━━ 💗᪲᪲᪲࣪ ִֶָ☾.ᯓᡣ𐭩🤍ྀི    ✝ 𝐀ɴᴛᴀ𝐑 𝐌ᴀɴ𝐓ᴀʀ 𝐒ʜᴀɪ𝐓ᴀɴ𝐈 𝐊ʜᴏ𝐏ᴀᴅ𝐀 {target} 𝐆ᴀ𝐑ɪ𝐁 𝐊ɪ 𝐀ᴍᴍ𝐈 𝐊ᴀ 𝐊ᴀʟ𝐀 𝐁ʜᴏs𝐃ᴀ  ━━━━━━━━ 💗᪲᪲᪲࣪ ִֶָ☾.ᯓᡣ𐭩🤍ྀི    ✝ 𝐀ɴᴛᴀ𝐑 𝐌ᴀɴ𝐓ᴀʀ 𝐒ʜᴀɪ𝐓ᴀɴ𝐈 𝐊ʜᴏ𝐏ᴀᴅ𝐀 {target} 𝐆ᴀ𝐑ɪ𝐁 𝐊ɪ 𝐀ᴍᴍ𝐈 𝐊ᴀ 𝐊ᴀʟ𝐀 𝐁ʜᴏs𝐃ᴀ  ━━━━━━━━ 💗᪲᪲᪲࣪ ִֶָ☾.ᯓᡣ𐭩🤍ྀི    ✝ 𝐀ɴᴛᴀ𝐑 𝐌ᴀɴ𝐓ᴀʀ 𝐒ʜᴀɪ𝐓ᴀɴ𝐈 𝐊ʜᴏ𝐏ᴀᴅ𝐀 {target} 𝐆ᴀ𝐑ɪ𝐁 𝐊ɪ 𝐀ᴍᴍ𝐈 𝐊ᴀ 𝐊ᴀʟ𝐀 𝐁ʜᴏs𝐃ᴀ  ━━━━━━━━ 💗᪲᪲᪲࣪ ִֶָ☾.ᯓᡣ𐭩🤍ྀི    ✝ 𝐀ɴᴛᴀ𝐑 𝐌ᴀɴ𝐓ᴀʀ 𝐒ʜᴀɪ𝐓ᴀɴ𝐈 𝐊ʜᴏ𝐏ᴀᴅ𝐀 {target} 𝐆ᴀ𝐑ɪ𝐁 𝐊ɪ 𝐀ᴍᴍ𝐈 𝐊ᴀ 𝐊ᴀʟ𝐀 𝐁ʜᴏs𝐃ᴀ  ━━━━━━━━ 💗᪲᪲᪲࣪ ִֶָ☾.ᯓᡣ𐭩🤍ྀི    ✝ 𝐀ɴᴛᴀ𝐑 𝐌ᴀɴ𝐓ᴀʀ 𝐒ʜᴀɪ𝐓ᴀɴ𝐈 𝐊ʜᴏ𝐏ᴀᴅ𝐀 {target} 𝐆ᴀ𝐑ɪ𝐁 𝐊ɪ 𝐀ᴍᴍ𝐈 𝐊ᴀ 𝐊ᴀʟ𝐀 𝐁ʜᴏs𝐃ᴀ  ━━━━━━━━ 💗᪲᪲᪲࣪ ִֶָ☾.ᯓᡣ𐭩🤍ྀི    ✝ 𝐀ɴᴛᴀ𝐑 𝐌ᴀɴ𝐓ᴀʀ 𝐒ʜᴀɪ𝐓ᴀɴ𝐈 𝐊ʜᴏ𝐏ᴀᴅ𝐀 {target} 𝐆ᴀ𝐑ɪ𝐁 𝐊ɪ 𝐀ᴍᴍ𝐈 𝐊ᴀ 𝐊ᴀʟ𝐀 𝐁ʜᴏs𝐃ᴀ  ━━━━━━━━ 💗᪲᪲᪲࣪ ִֶָ☾.ᯓᡣ𐭩🤍ྀི    ✝ 𝐀ɴᴛᴀ𝐑 𝐌ᴀɴ𝐓ᴀʀ 𝐒ʜᴀɪ𝐓ᴀɴ𝐈 𝐊ʜᴏ𝐏ᴀᴅ𝐀 {target} 𝐆ᴀ𝐑ɪ𝐁 𝐊ɪ 𝐀ᴍᴍ𝐈 𝐊ᴀ 𝐊ᴀʟ𝐀 𝐁ʜᴏs𝐃ᴀ  ━━━━━━━━ 💗᪲᪲᪲࣪ ִֶָ☾.ᯓᡣ𐭩🤍ྀི    ✝ 𝐀ɴᴛᴀ𝐑 𝐌ᴀɴ𝐓ᴀʀ 𝐒ʜᴀɪ𝐓ᴀɴ𝐈 𝐊ʜᴏ𝐏ᴀᴅ𝐀 {target} 𝐆ᴀ𝐑ɪ𝐁 𝐊ɪ 𝐀ᴍᴍ𝐈 𝐊ᴀ 𝐊ᴀʟ𝐀 𝐁ʜᴏs𝐃ᴀ  ━━━━━━━━ 💗᪲᪲᪲࣪ ִֶָ☾.ᯓᡣ𐭩🤍ྀི    ✝ 𝐀ɴᴛᴀ𝐑 𝐌ᴀɴ𝐓ᴀʀ 𝐒ʜᴀɪ𝐓ᴀɴ𝐈 𝐊ʜᴏ𝐏ᴀᴅ𝐀 {target} 𝐆ᴀ𝐑ɪ𝐁 𝐊ɪ 𝐀ᴍᴍ𝐈 𝐊ᴀ 𝐊ᴀʟ𝐀 𝐁ʜᴏs𝐃ᴀ  ━━━━━━━━ 💗᪲᪲᪲࣪ ִֶָ☾.ᯓᡣ𐭩🤍ྀི    ✝ 𝐀ɴᴛᴀ𝐑 𝐌ᴀɴ𝐓ᴀʀ 𝐒ʜᴀɪ𝐓ᴀɴ𝐈 𝐊ʜᴏ𝐏ᴀᴅ𝐀 {target} 𝐆ᴀ𝐑ɪ𝐁 𝐊ɪ 𝐀ᴍᴍ𝐈 𝐊ᴀ 𝐊ᴀʟ𝐀 𝐁ʜᴏs𝐃ᴀ  ━━━━━━━━ 💗᪲᪲᪲࣪ ִֶָ☾.ᯓᡣ𐭩🤍ྀི    ✝ 𝐀ɴᴛᴀ𝐑 𝐌ᴀɴ𝐓ᴀʀ 𝐒ʜᴀɪ𝐓ᴀɴ𝐈 𝐊ʜᴏ𝐏ᴀᴅ𝐀 {target} 𝐆ᴀ𝐑ɪ𝐁 𝐊ɪ 𝐀ᴍᴍ𝐈 𝐊ᴀ 𝐊ᴀʟ𝐀 𝐁ʜᴏs𝐃ᴀ  ━━━━━━━━ 💗᪲᪲᪲࣪ ִֶָ☾.ᯓᡣ𐭩🤍ྀི    ✝ 𝐀ɴᴛᴀ𝐑 𝐌ᴀɴ𝐓ᴀʀ 𝐒ʜᴀɪ𝐓ᴀɴ𝐈 𝐊ʜᴏ𝐏ᴀᴅ𝐀 {target} 𝐆ᴀ𝐑ɪ𝐁 𝐊ɪ 𝐀ᴍᴍ𝐈 𝐊ᴀ 𝐊ᴀʟ𝐀 𝐁ʜᴏs𝐃ᴀ  ━━━━━━━━ 💗᪲᪲᪲࣪ ִֶָ☾.ᯓᡣ𐭩🤍ྀི    ✝ 𝐀ɴᴛᴀ𝐑 𝐌ᴀɴ𝐓ᴀʀ 𝐒ʜᴀɪ𝐓ᴀɴ𝐈 𝐊ʜᴏ𝐏ᴀᴅ𝐀 {target} 𝐆ᴀ𝐑ɪ𝐁 𝐊ɪ 𝐀ᴍᴍ𝐈 𝐊ᴀ 𝐊ᴀʟ𝐀 𝐁ʜᴏs𝐃ᴀ  ━━━━━━━━ 💗᪲᪲᪲࣪ ִֶָ☾.ᯓᡣ𐭩🤍ྀི    ✝ 𝐀ɴᴛᴀ𝐑 𝐌ᴀɴ𝐓ᴀʀ 𝐒ʜᴀɪ𝐓ᴀɴ𝐈 𝐊ʜᴏ𝐏ᴀᴅ𝐀 {target} 𝐆ᴀ𝐑ɪ𝐁 𝐊ɪ 𝐀ᴍᴍ𝐈 𝐊ᴀ 𝐊ᴀʟ𝐀 𝐁ʜᴏs𝐃ᴀ  ━━━━━━━━ 💗᪲᪲᪲࣪ ִֶָ☾.ᯓᡣ𐭩🤍ྀི    ✝ 𝐀ɴᴛᴀ𝐑 𝐌ᴀɴ𝐓ᴀʀ 𝐒ʜᴀɪ𝐓ᴀɴ𝐈 𝐊ʜᴏ𝐏ᴀᴅ𝐀 {target} 𝐆ᴀ𝐑ɪ𝐁 𝐊ɪ 𝐀ᴍᴍ𝐈 𝐊ᴀ 𝐊ᴀʟ𝐀 𝐁ʜᴏs𝐃ᴀ  ━━━━━━━━ 💗᪲᪲᪲࣪ ִֶָ☾.ᯓᡣ𐭩🤍ྀི    ✝ 𝐀ɴᴛᴀ𝐑 𝐌ᴀɴ𝐓ᴀʀ 𝐒ʜᴀɪ𝐓ᴀɴ𝐈 𝐊ʜᴏ𝐏ᴀᴅ𝐀 {target} 𝐆ᴀ𝐑ɪ𝐁 𝐊ɪ 𝐀ᴍᴍ𝐈 𝐊ᴀ 𝐊ᴀʟ𝐀 𝐁ʜᴏs𝐃ᴀ  ━━━━━━━━ 💗᪲᪲᪲࣪ ִֶָ☾.ᯓᡣ𐭩🤍ྀི    ✝ 𝐀ɴᴛᴀ𝐑 𝐌ᴀɴ𝐓ᴀʀ 𝐒ʜᴀɪ𝐓ᴀɴ𝐈 𝐊ʜᴏ𝐏ᴀᴅ𝐀 {target} 𝐆ᴀ𝐑ɪ𝐁 𝐊ɪ 𝐀ᴍᴍ𝐈 𝐊ᴀ 𝐊ᴀʟ𝐀 𝐁ʜᴏs𝐃ᴀ  ━━━━━━━━ 💗᪲᪲᪲࣪ ִֶָ☾.ᯓᡣ𐭩🤍ྀི    ✝ 𝐀ɴᴛᴀ𝐑 𝐌ᴀɴ𝐓ᴀʀ 𝐒ʜᴀɪ𝐓ᴀɴ𝐈 𝐊ʜᴏ𝐏ᴀᴅ𝐀 {target} 𝐆ᴀ𝐑ɪ𝐁 𝐊ɪ 𝐀ᴍᴍ𝐈 𝐊ᴀ 𝐊ᴀʟ𝐀 𝐁ʜᴏs𝐃ᴀ  ━━━━━━━━ 💗᪲᪲᪲࣪ ִֶָ☾.ᯓᡣ𐭩🤍ྀི    ✝ 𝐀ɴᴛᴀ𝐑 𝐌ᴀɴ𝐓ᴀʀ 𝐒ʜᴀɪ𝐓ᴀɴ𝐈 𝐊ʜᴏ𝐏ᴀᴅ𝐀 {target} 𝐆ᴀ𝐑ɪ𝐁 𝐊ɪ 𝐀ᴍᴍ𝐈 𝐊ᴀ 𝐊ᴀʟ𝐀 𝐁ʜᴏs𝐃ᴀ  ━━━━━━━━ 💗᪲᪲᪲࣪ ִֶָ☾.ᯓᡣ𐭩🤍ྀི    ✝ 𝐀ɴᴛᴀ𝐑 𝐌ᴀɴ𝐓ᴀʀ 𝐒ʜᴀɪ𝐓ᴀɴ𝐈 𝐊ʜᴏ𝐏ᴀᴅ𝐀 {target} 𝐆ᴀ𝐑ɪ𝐁 𝐊ɪ 𝐀ᴍᴍ𝐈 𝐊ᴀ 𝐊ᴀʟ𝐀 𝐁ʜᴏs𝐃ᴀ  ━━━━━━━━ 💗᪲᪲᪲࣪ ִֶָ☾.ᯓᡣ𐭩🤍ྀི    ✝ 𝐀ɴᴛᴀ𝐑 𝐌ᴀɴ𝐓ᴀʀ 𝐒ʜᴀɪ𝐓ᴀɴ𝐈 𝐊ʜᴏ𝐏ᴀᴅ𝐀 {target} 𝐆ᴀ𝐑ɪ𝐁 𝐊ɪ 𝐀ᴍᴍ𝐈 𝐊ᴀ 𝐊ᴀʟ𝐀 𝐁ʜᴏs𝐃ᴀ  ━━━━━━━━ 💗᪲᪲᪲࣪ ִֶָ☾.ᯓᡣ𐭩🤍ྀི    ✝ 𝐀ɴᴛᴀ𝐑 𝐌ᴀɴ𝐓ᴀʀ 𝐒ʜᴀɪ𝐓ᴀɴ𝐈 𝐊ʜᴏ𝐏ᴀᴅ𝐀 {target} 𝐆ᴀ𝐑ɪ𝐁 𝐊ɪ 𝐀ᴍᴍ𝐈 𝐊ᴀ 𝐊ᴀʟ𝐀 𝐁ʜᴏs𝐃ᴀ  ━━━━━━━━ 💗᪲᪲᪲࣪ ִֶָ☾.ᯓᡣ𐭩🤍ྀི    ✝ 𝐀ɴᴛᴀ𝐑 𝐌ᴀɴ𝐓ᴀʀ 𝐒ʜᴀɪ𝐓ᴀɴ𝐈 𝐊ʜᴏ𝐏ᴀᴅ𝐀 {target} 𝐆ᴀ𝐑ɪ𝐁 𝐊ɪ 𝐀ᴍᴍ𝐈 𝐊ᴀ 𝐊ᴀʟ𝐀 𝐁ʜᴏs𝐃ᴀ  ━━━━━━━━ 💗᪲᪲᪲࣪ ִֶָ☾.ᯓᡣ𐭩🤍ྀི    ✝ 𝐀ɴᴛᴀ𝐑 𝐌ᴀɴ𝐓ᴀʀ 𝐒ʜᴀɪ𝐓ᴀɴ𝐈 𝐊ʜᴏ𝐏ᴀᴅ𝐀 {target} 𝐆ᴀ𝐑ɪ𝐁 𝐊ɪ 𝐀ᴍᴍ𝐈 𝐊ᴀ 𝐊ᴀʟ𝐀 𝐁ʜᴏs𝐃ᴀ  ━━━━━━━━ 💗᪲᪲᪲࣪ ִֶָ☾.ᯓᡣ𐭩🤍ྀི    ✝ 𝐀ɴᴛᴀ𝐑 𝐌ᴀɴ𝐓ᴀʀ 𝐒ʜᴀɪ𝐓ᴀɴ𝐈 𝐊ʜᴏ𝐏ᴀᴅ𝐀 {target} 𝐆ᴀ𝐑ɪ𝐁 𝐊ɪ 𝐀ᴍᴍ𝐈 𝐊ᴀ 𝐊ᴀʟ𝐀 𝐁ʜᴏs𝐃ᴀ  ━━━━━━━━ 💗᪲᪲᪲࣪ ִֶָ☾.ᯓᡣ𐭩🤍ྀི    ✝ 𝐀ɴᴛᴀ𝐑 𝐌ᴀɴ𝐓ᴀʀ 𝐒ʜᴀɪ𝐓ᴀɴ𝐈 𝐊ʜᴏ𝐏ᴀᴅ𝐀 {target} 𝐆ᴀ𝐑ɪ𝐁 𝐊ɪ 𝐀ᴍᴍ𝐈 𝐊ᴀ 𝐊ᴀʟ𝐀 𝐁ʜᴏs𝐃ᴀ  ━━━━━━━━ 💗᪲᪲᪲࣪ ִֶָ☾.ᯓᡣ𐭩🤍ྀི    ✝ 𝐀ɴᴛᴀ𝐑 𝐌ᴀɴ𝐓ᴀʀ 𝐒ʜᴀɪ𝐓ᴀɴ𝐈 𝐊ʜᴏ𝐏ᴀᴅ𝐀 {target} 𝐆ᴀ𝐑ɪ𝐁 𝐊ɪ 𝐀ᴍᴍ𝐈 𝐊ᴀ 𝐊ᴀʟ𝐀 𝐁ʜᴏs𝐃ᴀ  ━━━━━━━━ 💗᪲᪲᪲࣪ ִֶָ☾.ᯓᡣ𐭩🤍ྀི    ✝ 𝐀ɴᴛᴀ𝐑 𝐌ᴀɴ𝐓ᴀʀ 𝐒ʜᴀɪ𝐓ᴀɴ𝐈 𝐊ʜᴏ𝐏ᴀᴅ𝐀 {target} 𝐆ᴀ𝐑ɪ𝐁 𝐊ɪ 𝐀ᴍᴍ𝐈 𝐊ᴀ 𝐊ᴀʟ𝐀 𝐁ʜᴏs𝐃ᴀ  ━━━━━━━━ 💗᪲᪲᪲࣪ ִֶָ☾.ᯓᡣ𐭩🤍ྀི    ✝ 𝐀ɴᴛᴀ𝐑 𝐌ᴀɴ𝐓ᴀʀ 𝐒ʜᴀɪ𝐓ᴀɴ𝐈 𝐊ʜᴏ𝐏ᴀᴅ𝐀 {target} 𝐆ᴀ𝐑ɪ𝐁 𝐊ɪ 𝐀ᴍᴍ𝐈 𝐊ᴀ 𝐊ᴀʟ𝐀 𝐁ʜᴏs𝐃ᴀ  ━━━━━━━━ 💗᪲᪲᪲࣪ ִֶָ☾.ᯓᡣ𐭩🤍ྀི    ✝ 𝐀ɴᴛᴀ𝐑 𝐌ᴀɴ𝐓ᴀʀ 𝐒ʜᴀɪ𝐓ᴀɴ𝐈 𝐊ʜᴏ𝐏ᴀᴅ𝐀 {target} 𝐆ᴀ𝐑ɪ𝐁 𝐊ɪ 𝐀ᴍᴍ𝐈 𝐊ᴀ 𝐊ᴀʟ𝐀 𝐁ʜᴏs𝐃ᴀ  ━━━━━━━━ 💗᪲᪲᪲࣪ ִֶָ☾.ᯓᡣ𐭩🤍ྀི    ✝ 𝐀ɴᴛᴀ𝐑 𝐌ᴀɴ𝐓ᴀʀ 𝐒ʜᴀɪ𝐓ᴀɴ𝐈 𝐊ʜᴏ𝐏ᴀᴅ𝐀 {target} 𝐆ᴀ𝐑ɪ𝐁 𝐊ɪ 𝐀ᴍᴍ𝐈 𝐊ᴀ 𝐊ᴀʟ𝐀 𝐁ʜᴏs𝐃ᴀ  ━━━━━━━━ 💗᪲᪲᪲࣪ ִֶָ☾.ᯓᡣ𐭩🤍ྀི",
    "➶　　　　　　　➶　　　　　　➶　　　　　➶　　　　　　　　　➤　➷　　　　　　　　➷　　　　 　　　➷　　　　　　➷　　　　　　　　　　　　　　➷{target} 𝙏𝙀𝙍𝙄 𝙈𝘼𝘼 \ 𝘽𝘼𝙃𝘼𝙉 𝘿𝙊𝙉𝙊 𝙆𝙊 𝙍𝘼𝙉𝘿𝙄 𝙆𝙊 𝘾𝙃𝙊𝘿𝙐 🤣　➶　　　　　　　➶　　　　　　➶　　　　　➶　　　　　　　　　➤　➷　　　　　　　　➷　　　　 　　　➷　　　　　　➷　　　　　　　　　　　　　　➷➶　　　　　　　➶　　　　　　➶　　　　　➶　　　　　　　　　➤　➷　　　　　　　　➷　　　　 　　　➷　　　　　　➷　　　　　　　　　　　　　　➷{target} 𝙏𝙀𝙍𝙄 𝙈𝘼𝘼 \ 𝘽𝘼𝙃𝘼𝙉 𝘿𝙊𝙉𝙊 𝙆𝙊 𝙍𝘼𝙉𝘿𝙄 𝙆𝙊 𝘾𝙃𝙊𝘿𝙐 🤣　➶　　　　　　　➶　　　　　　➶　　　　　➶　　　　　　　　　➤　➷　　　　　　　　➷　　　　 　　　➷　　　　　　➷　　　　　　　　　　　　　　➷➶　　　　　　　➶　　　　　　➶　　　　　➶　　　　　　　　　➤　➷　　　　　　　　➷　　　　 　　　➷　　　　　　➷　　　　　　　　　　　　　　➷{target} 𝙏𝙀𝙍𝙄 𝙈𝘼𝘼 \ 𝘽𝘼𝙃𝘼𝙉 𝘿𝙊𝙉𝙊 𝙆𝙊 𝙍𝘼𝙉𝘿𝙄 𝙆𝙊 𝘾𝙃𝙊𝘿𝙐 🤣　➶　　　　　　　➶　　　　　　➶　　　　　➶　　　　　　　　　➤　➷　　　　　　　　➷　　　　 　　　➷　　　　　　➷　　　　　　　　　　　　　　➷➶　　　　　　　➶　　　　　　➶　　　　　➶　　　　　　　　　➤　➷　　　　　　　　➷　　　　 　　　➷　　　　　　➷　　　　　　　　　　　　　　➷{target} 𝙏𝙀𝙍𝙄 𝙈𝘼𝘼 \ 𝘽𝘼𝙃𝘼𝙉 𝘿𝙊𝙉𝙊 𝙆𝙊 𝙍𝘼𝙉𝘿𝙄 𝙆𝙊 𝘾𝙃𝙊𝘿𝙐 🤣　➶　　　　　　　➶　　　　　　➶　　　　　➶　　　　　　　　　➤　➷　　　　　　　　➷　　　　 　　　➷　　　　　　➷　　　　　　　　　　　　　　➷➶　　　　　　　➶　　　　　　➶　　　　　➶　　　　　　　　　➤　➷　　　　　　　　➷　　　　 　　　➷",
  "➶　　　　　　　➶　　　　　　➶　　　　　➶　　　　　　　　　➤　➷　　　　　　　　➷　　　　 　　　➷　　　　　　➷　　　　　　　　　　　　　　➷{target} 𝙏𝙀𝙍𝙄 𝙈𝘼𝘼 \ 𝘽𝘼𝙃𝘼𝙉 𝘿𝙊𝙉𝙊 𝙆𝙊 𝙍𝘼𝙉𝘿𝙄 𝙆𝙊 𝘾𝙃𝙊𝘿𝙐👅　➶　　　　　　　➶　　　　　　➶　　　　　➶　　　　　　　　　➤　➷　　　　　　　　➷　　　　 　　　➷　　　　　　➷　　　　　　　　　　　　　　➷➶　　　　　　　➶　　　　　　➶　　　　　➶　　　　　　　　　➤　➷　　　　　　　　➷　　　　 　　　➷　　　　　　➷　　　　　　　　　　　　　　➷{target} 𝙏𝙀𝙍𝙄 𝙈𝘼𝘼 \ 𝘽𝘼𝙃𝘼𝙉 𝘿𝙊𝙉𝙊 𝙆𝙊 𝙍𝘼𝙉𝘿𝙄 𝙆𝙊 𝘾𝙃𝙊𝘿𝙐👅　➶　　　　　　　➶　　　　　　➶　　　　　➶　　　　　　　　　➤　➷　　　　　　　　➷　　　　 　　　➷　　　　　　➷　　　　　　　　　　　　　　➷➶　　　　　　　➶　　　　　　➶　　　　　➶　　　　　　　　　➤　➷　　　　　　　　➷　　　　 　　　➷　　　　　　➷　　　　　　　　　　　　　　➷{target} 𝙏𝙀𝙍𝙄 𝙈𝘼𝘼 \ 𝘽𝘼𝙃𝘼𝙉 𝘿𝙊𝙉𝙊 𝙆𝙊 𝙍𝘼𝙉𝘿𝙄 𝙆𝙊 𝘾𝙃𝙊𝘿𝙐👅　➶　　　　　　　➶　　　　　　➶　　　　　➶　　　　　　　　　➤　➷　　　　　　　　➷　　　　 　　　➷　　　　　　➷　　　　　　　　　　　　　　➷➶　　　　　　　➶　　　　　　➶　　　　　➶　　　　　　　　　➤　➷　　　　　　　　➷　　　　 　　　➷　　　　　　➷　　　　　　　　　　　　　　➷{target} 𝙏𝙀𝙍𝙄 𝙈𝘼𝘼 \ 𝘽𝘼𝙃𝘼𝙉 𝘿𝙊𝙉𝙊 𝙆𝙊 𝙍𝘼𝙉𝘿𝙄 𝙆𝙊 𝘾𝙃𝙊𝘿𝙐👅　➶　　　　　　　➶　　　　　　➶　　　　　➶　　　　　　　　　➤　➷　　　　　　　　➷　　　　 　　　➷　　　　　　➷　　　　　　　　　　　　　　➷➶　　　　　　　➶　　　　　　➶　　　　　➶　　　　　　　　　➤　➷　　　　　　　　➷　　　　 　　　➷",
"➶　　　　　　　➶　　　　　　➶　　　　　➶　　　　　　　　　➤　➷　　　　　　　　➷　　　　 　　　➷　　　　　　➷　　　　　　　　　　　　　　➷{target} 𝙏𝙀𝙍𝙄 𝙈𝘼𝘼 \ 𝘽𝘼𝙃𝘼𝙉 𝘿𝙊𝙉𝙊 𝙆𝙊 𝙍𝘼𝙉𝘿𝙄 𝙆𝙊 𝘾𝙃𝙊𝘿𝙐👅　➶　　　　　　　➶　　　　　　➶　　　　　➶　　　　　　　　　➤　➷　　　　　　　　➷　　　　 　　　➷　　　　　　➷　　　　　　　　　　　　　　➷➶　　　　　　　➶　　　　　　➶　　　　　➶　　　　　　　　　➤　➷　　　　　　　　➷　　　　 　　　➷　　　　　　➷　　　　　　　　　　　　　　➷{target} 𝙏𝙀𝙍𝙄 𝙈𝘼𝘼 \ 𝘽𝘼𝙃𝘼𝙉 𝘿𝙊𝙉𝙊 𝙆𝙊 𝙍𝘼𝙉𝘿𝙄 𝙆𝙊 𝘾𝙃𝙊𝘿𝙐👅　➶　　　　　　　➶　　　　　　➶　　　　　➶　　　　　　　　　➤　➷　　　　　　　　➷　　　　 　　　➷　　　　　　➷　　　　　　　　　　　　　　➷➶　　　　　　　➶　　　　　　➶　　　　　➶　　　　　　　　　➤　➷　　　　　　　　➷　　　　 　　　➷　　　　　　➷　　　　　　　　　　　　　　➷{target} 𝙏𝙀𝙍𝙄 𝙈𝘼𝘼 \ 𝘽𝘼𝙃𝘼𝙉 𝘿𝙊𝙉𝙊 𝙆𝙊 𝙍𝘼𝙉𝘿𝙄 𝙆𝙊 𝘾𝙃𝙊𝘿𝙐👅　➶　　　　　　　➶　　　　　　➶　　　　　➶　　　　　　　　　➤　➷　　　　　　　　➷　　　　 　　　➷　　　　　　➷　　　　　　　　　　　　　　➷➶　　　　　　　➶　　　　　　➶　　　　　➶　　　　　　　　　➤　➷　　　　　　　　➷　　　　 　　　➷　　　　　　➷　　　　　　　　　　　　　　➷{target} 𝙏𝙀𝙍𝙄 𝙈𝘼𝘼 \ 𝘽𝘼𝙃𝘼𝙉 𝘿𝙊𝙉𝙊 𝙆𝙊 𝙍𝘼𝙉𝘿𝙄 𝙆𝙊 𝘾𝙃𝙊𝘿𝙐👅　➶",
"{target} 𝐓𝐄𝐑𝐈 𝐌𝐀𝐀_𝐁𝐀𝐇𝐀𝐍 𝐊𝐎 𝐂𝐇𝐎𝐃𝐔 𝐁𝐈𝐍𝐀 𝐂𝐎𝐍𝐃𝐎𝐌 𝐊𝐄 😝 𝐇𝐀𝐇𝐀𝐇𝐀 ׂׂૢ🩵__{target}   𝐓𝐄𝐑𝐈 𝐌𝐀𝐀_𝐁𝐀𝐇𝐀𝐍 𝐊𝐎 𝐂𝐇𝐎𝐃𝐔 𝐁𝐈𝐍𝐀 𝐂𝐎𝐍𝐃𝐎𝐌 𝐊𝐄 😝 𝐇𝐀𝐇𝐀𝐇𝐀 ׂׂૢ🩵__{target}   𝐓𝐄𝐑𝐈 𝐌𝐀𝐀_𝐁𝐀𝐇𝐀𝐍 𝐊𝐎 𝐂𝐇𝐎𝐃𝐔 𝐁𝐈𝐍𝐀 𝐂𝐎𝐍𝐃𝐎𝐌 𝐊𝐄 😝 𝐇𝐀𝐇𝐀𝐇𝐀 ׂׂૢ🩵__{target}   𝐓𝐄𝐑𝐈 𝐌𝐀𝐀_𝐁𝐀𝐇𝐀𝐍 𝐊𝐎 𝐂𝐇𝐎𝐃𝐔 𝐁𝐈𝐍𝐀 𝐂𝐎𝐍𝐃𝐎𝐌 𝐊𝐄 😝 𝐇𝐀𝐇𝐀𝐇𝐀 ׂׂૢ🩵__{target}   𝐓𝐄𝐑𝐈 𝐌𝐀𝐀_𝐁𝐀𝐇𝐀𝐍 𝐊𝐎 𝐂𝐇𝐎𝐃𝐔 𝐁𝐈𝐍𝐀 𝐂𝐎𝐍𝐃𝐎𝐌 𝐊𝐄 😝 𝐇𝐀𝐇𝐀𝐇𝐀 ׂׂૢ🩵__{target}   𝐓𝐄𝐑𝐈 𝐌𝐀𝐀_𝐁𝐀𝐇𝐀𝐍 𝐊𝐎 𝐂𝐇𝐎𝐃𝐔 𝐁𝐈𝐍𝐀 𝐂𝐎𝐍𝐃𝐎𝐌 𝐊𝐄 😝 𝐇𝐀𝐇𝐀𝐇𝐀 ׂׂૢ🩵__{target}   𝐓𝐄𝐑𝐈 𝐌𝐀𝐀_𝐁𝐀𝐇𝐀𝐍 𝐊𝐎 𝐂𝐇𝐎𝐃𝐔 𝐁𝐈𝐍𝐀 𝐂𝐎𝐍𝐃𝐎𝐌 𝐊𝐄 😝 𝐇𝐀𝐇𝐀𝐇𝐀 ׂׂૢ🩵__{target}   𝐓𝐄𝐑𝐈 𝐌𝐀𝐀_𝐁𝐀𝐇𝐀𝐍 𝐊𝐎 𝐂𝐇𝐎𝐃𝐔 𝐁𝐈𝐍𝐀 𝐂𝐎𝐍𝐃𝐎𝐌 𝐊𝐄 😝 𝐇𝐀𝐇𝐀𝐇𝐀 ׂׂૢ🩵__{target}   𝐓𝐄𝐑𝐈 𝐌𝐀𝐀_𝐁𝐀𝐇𝐀𝐍 𝐊𝐎 𝐂𝐇𝐎𝐃𝐔 𝐁𝐈𝐍𝐀 𝐂𝐎𝐍𝐃𝐎𝐌 𝐊𝐄 😝 𝐇𝐀𝐇𝐀𝐇𝐀 ׂׂૢ🩵__{target}   𝐓𝐄𝐑𝐈 𝐌𝐀𝐀_𝐁𝐀𝐇𝐀𝐍 𝐊𝐎 𝐂𝐇𝐎𝐃𝐔 𝐁𝐈𝐍𝐀 𝐂𝐎𝐍𝐃𝐎𝐌 𝐊𝐄 😝 𝐇𝐀𝐇𝐀𝐇𝐀 ׂׂૢ🩵__{target}   𝐓𝐄𝐑𝐈 𝐌𝐀𝐀_𝐁𝐀𝐇𝐀𝐍 𝐊𝐎 𝐂𝐇𝐎𝐃𝐔 𝐁𝐈𝐍𝐀 𝐂𝐎𝐍𝐃𝐎𝐌 𝐊𝐄 😝 𝐇𝐀𝐇𝐀𝐇𝐀 ׂׂૢ🩵__{target}   𝐓𝐄𝐑𝐈 𝐌𝐀𝐀_𝐁𝐀𝐇𝐀𝐍 𝐊𝐎 𝐂𝐇𝐎𝐃𝐔 𝐁𝐈𝐍𝐀 𝐂𝐎𝐍𝐃𝐎𝐌 𝐊𝐄 😝 𝐇𝐀𝐇𝐀𝐇𝐀 ׂׂૢ🩵___",
  "{target} 𝐓𝐄𝐑𝐈 𝐌𝐀𝐀_𝐁𝐀𝐇𝐀𝐍 𝐊𝐎 𝐂𝐇𝐎𝐃𝐔 𝐁𝐈𝐍𝐀 𝐂𝐎𝐍𝐃𝐎𝐌 𝐊𝐄 😝 𝐇𝐀𝐇𝐀𝐇𝐀 ׂׂૢ🩵__{target}   𝐓𝐄𝐑𝐈 𝐌𝐀𝐀_𝐁𝐀𝐇𝐀𝐍 𝐊𝐎 𝐂𝐇𝐎𝐃𝐔 𝐁𝐈𝐍𝐀 𝐂𝐎𝐍𝐃𝐎𝐌 𝐊𝐄 😝 𝐇𝐀𝐇𝐀𝐇𝐀 ׂׂૢ🩵__{target}   𝐓𝐄𝐑𝐈 𝐌𝐀𝐀_𝐁𝐀𝐇𝐀𝐍 𝐊𝐎 𝐂𝐇𝐎𝐃𝐔 𝐁𝐈𝐍𝐀 𝐂𝐎𝐍𝐃𝐎𝐌 𝐊𝐄 😝 𝐇𝐀𝐇𝐀𝐇𝐀 ׂׂૢ🩵__{target}   𝐓𝐄𝐑𝐈 𝐌𝐀𝐀_𝐁𝐀𝐇𝐀𝐍 𝐊𝐎 𝐂𝐇𝐎𝐃𝐔 𝐁𝐈𝐍𝐀 𝐂𝐎𝐍𝐃𝐎𝐌 𝐊𝐄 😝 𝐇𝐀𝐇𝐀𝐇𝐀 ׂׂૢ🩵__{target}   𝐓𝐄𝐑𝐈 𝐌𝐀𝐀_𝐁𝐀𝐇𝐀𝐍 𝐊𝐎 𝐂𝐇𝐎𝐃𝐔 𝐁𝐈𝐍𝐀 𝐂𝐎𝐍𝐃𝐎𝐌 𝐊𝐄 😝 𝐇𝐀𝐇𝐀𝐇𝐀 ׂׂૢ🩵__{target}   𝐓𝐄𝐑𝐈 𝐌𝐀𝐀_𝐁𝐀𝐇𝐀𝐍 𝐊𝐎 𝐂𝐇𝐎𝐃𝐔 𝐁𝐈𝐍𝐀 𝐂𝐎𝐍𝐃𝐎𝐌 𝐊𝐄 😝 𝐇𝐀𝐇𝐀𝐇𝐀 ׂׂૢ🩵__{target}   𝐓𝐄𝐑𝐈 𝐌𝐀𝐀_𝐁𝐀𝐇𝐀𝐍 𝐊𝐎 𝐂𝐇𝐎𝐃𝐔 𝐁𝐈𝐍𝐀 𝐂𝐎𝐍𝐃𝐎𝐌 𝐊𝐄 😝 𝐇𝐀𝐇𝐀𝐇𝐀 ׂׂૢ🩵__{target}   𝐓𝐄𝐑𝐈 𝐌𝐀𝐀_𝐁𝐀𝐇𝐀𝐍 𝐊𝐎 𝐂𝐇𝐎𝐃𝐔 𝐁𝐈𝐍𝐀 𝐂𝐎𝐍𝐃𝐎𝐌 𝐊𝐄 😝 𝐇𝐀𝐇𝐀𝐇𝐀 ׂׂૢ🩵__{target}   𝐓𝐄𝐑𝐈 𝐌𝐀𝐀_𝐁𝐀𝐇𝐀𝐍 𝐊𝐎 𝐂𝐇𝐎𝐃𝐔 𝐁𝐈𝐍𝐀 𝐂𝐎𝐍𝐃𝐎𝐌 𝐊𝐄 😝 𝐇𝐀𝐇𝐀𝐇𝐀 ׂׂૢ🩵__{target}   𝐓𝐄𝐑𝐈 𝐌𝐀𝐀_𝐁𝐀𝐇𝐀𝐍 𝐊𝐎 𝐂𝐇𝐎𝐃𝐔 𝐁𝐈𝐍𝐀 𝐂𝐎𝐍𝐃𝐎𝐌 𝐊𝐄 😝 𝐇𝐀𝐇𝐀𝐇𝐀 ׂׂૢ🩵__{target}   𝐓𝐄𝐑𝐈 𝐌𝐀𝐀_𝐁𝐀𝐇𝐀𝐍 𝐊𝐎 𝐂𝐇𝐎𝐃𝐔 𝐁𝐈𝐍𝐀 𝐂𝐎𝐍𝐃𝐎𝐌 𝐊𝐄 😝 𝐇𝐀𝐇𝐀𝐇𝐀 ׂׂૢ🩵__{target}   𝐓𝐄𝐑𝐈 𝐌𝐀𝐀_𝐁𝐀𝐇𝐀𝐍 𝐊𝐎 𝐂𝐇𝐎𝐃𝐔 𝐁𝐈𝐍𝐀 𝐂𝐎𝐍𝐃𝐎𝐌 𝐊𝐄 😝 𝐇𝐀𝐇𝐀𝐇𝐀 ׂׂૢ🩵___"""
]

# PRELOADER FOR IMAGESPAM & PFP
PRELOADED_IMAGES: List[bytes] = []

def preload_images(count: int = 50):
    print(f"⏳ Pre-loading {count} images for ultra-fast spam...")
    try:
        from PIL import Image
        for _ in range(count):
            color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
            img = Image.new("RGB", (200, 200), color)
            buf = io.BytesIO()
            img.save(buf, format="JPEG")
            PRELOADED_IMAGES.append(buf.getvalue())
        print(f"✅ {len(PRELOADED_IMAGES)} Images loaded into RAM successfully!")
    except Exception as e:
        print(f"❌ Failed to preload images (PIL not installed?): {e}")

ALL_BOT_INSTANCES: Dict[int, 'HyperBotInstance'] = {}
GLOBAL_STOP_EVENT = asyncio.Event()
COMMAND_LOCKS: Dict[int, asyncio.Lock] = {}

def get_command_lock(chat_id: int) -> asyncio.Lock:
    if chat_id not in COMMAND_LOCKS:
        COMMAND_LOCKS[chat_id] = asyncio.Lock()
    return COMMAND_LOCKS[chat_id]

class HyperBotInstance:
    def __init__(self, bot_number, owner_id):
        self.bot_number = bot_number
        self.owner_id = owner_id
        self.authorized_users = set(DEFAULT_AUTHORIZED_USERS)
        
        # TASK TRACKERS
        self.active_spam_tasks: Dict[int, List[asyncio.Task]] = {}
        self.active_name_change_tasks: Dict[int, List[asyncio.Task]] = {}
        self.active_custom_nc_tasks: Dict[int, List[asyncio.Task]] = {}
        self.active_reply_tasks: Dict[int, asyncio.Task] = {}
        self.active_imagespam_tasks: Dict[int, List[asyncio.Task]] = {}
        self.active_slide_tasks: Dict[int, List[asyncio.Task]] = {}
        self.active_pfp_tasks: Dict[int, asyncio.Task] = {}
        
        # TARGET TRACKERS
        self.active_reply_targets: Dict[int, str] = {}
        self.pending_replies: Dict[int, List[int]] = {}
        self.delete_targets: Dict[int, Set[str]] = {}
        self.auto_react_targets: Dict[int, Set[int]] = {}
        
        self.chat_delays: Dict[int, float] = {}
        self.chat_threads: Dict[int, int] = {}
        self.locks: Dict[int, asyncio.Lock] = {}
        self.stats = {"sent": 0, "errors": 0, "start_time": time.time()}
        self.is_running = True
        ALL_BOT_INSTANCES[bot_number] = self

    def get_lock(self, chat_id):
        if chat_id not in self.locks:
            self.locks[chat_id] = asyncio.Lock()
        return self.locks[chat_id]

    async def check_owner(self, update):
        user_id = update.effective_user.id
        if not (user_id == self.owner_id or user_id in self.authorized_users):
            return False
        return True

    async def check_main_owner(self, update):
        if update.effective_user.id != self.owner_id:
            return False
        return True

    async def safe_cancel_tasks(self, tasks: List[asyncio.Task]):
        for task in tasks:
            if not task.done(): task.cancel()
        for task in tasks:
            try: await asyncio.wait_for(asyncio.shield(task), timeout=2.0)
            except: pass

    async def stop_all_tasks_globally(self):
        all_tasks = []
        for d in [self.active_spam_tasks, self.active_name_change_tasks, self.active_custom_nc_tasks, 
                  self.active_imagespam_tasks, self.active_slide_tasks]:
            for tasks in list(d.values()): all_tasks.extend(tasks)
            d.clear()
            
        for d in [self.active_reply_tasks, self.active_pfp_tasks]:
            for task in list(d.values()): all_tasks.append(task)
            d.clear()
            
        self.active_reply_targets.clear()
        self.pending_replies.clear()
        
        await self.safe_cancel_tasks(all_tasks)
        return len(all_tasks)

    # ------------------ LOOP ENGINES ------------------

    async def name_change_loop(self, chat_id, base_name, context, worker_id=1, mode="normal"):
        msg_index = 0
        while True:
            try:
                while self.is_running and not GLOBAL_STOP_EVENT.is_set():
                    delay = self.chat_delays.get(chat_id, 0)
                    try:
                        if mode == "godspeed":
                            display_name = random.choice(GODSPEED_NAMES)
                        elif mode == "exonc":
                            display_name = f"{random.choice(GODSPEED_NAMES)} {random.choice(NAME_CHANGE_MESSAGES).split()[0]}"[:255]
                        elif mode == "ncbaap":
                            display_name = random.choice(NAME_CHANGE_MESSAGES).format(target=base_name)[:255]
                        else:
                            current_msg = NAME_CHANGE_MESSAGES[msg_index % len(NAME_CHANGE_MESSAGES)]
                            display_name = current_msg.format(target=base_name)[:255]

                        await context.bot.set_chat_title(chat_id=chat_id, title=display_name)
                        msg_index += 1
                        self.stats["sent"] += 1
                        if delay > 0: await asyncio.sleep(delay)
                    except asyncio.CancelledError: raise
                    except RetryAfter as e: await asyncio.sleep(int(e.retry_after) + 0.05)
                    except (TimedOut, NetworkError): pass
                    except (BadRequest, Forbidden): await asyncio.sleep(0.1); msg_index += 1
                    except Exception: self.stats["errors"] += 1; msg_index += 1
                break
            except asyncio.CancelledError: break
            except Exception: await asyncio.sleep(0.1)

    async def spam_loop(self, chat_id, target_name, context, worker_id, mode="text"):
        while True:
            try:
                while self.is_running and not GLOBAL_STOP_EVENT.is_set():
                    delay = self.chat_delays.get(chat_id, 0)
                    try:
                        if mode == "image" and PRELOADED_IMAGES:
                            img_bytes = random.choice(PRELOADED_IMAGES)
                            await context.bot.send_photo(chat_id=chat_id, photo=img_bytes, caption=f"⚡ HYPER-X SPAM #{random.randint(1,999)}")
                        else:
                            spam_msg = random.choice(SPAM_MESSAGES).format(target=target_name)
                            await context.bot.send_message(chat_id=chat_id, text=spam_msg)
                            
                        self.stats["sent"] += 1
                        if delay > 0: await asyncio.sleep(delay)
                    except asyncio.CancelledError: raise
                    except RetryAfter as e: await asyncio.sleep(int(e.retry_after) + 0.05)
                    except (TimedOut, NetworkError): pass
                    except (BadRequest, Forbidden): await asyncio.sleep(0.1)
                    except Exception: self.stats["errors"] += 1
                break
            except asyncio.CancelledError: break
            except Exception: await asyncio.sleep(0.1)

    async def slide_loop(self, chat_id, target_name, context, worker_id):
        last_id = None
        while True:
            try:
                while self.is_running and not GLOBAL_STOP_EVENT.is_set():
                    delay = self.chat_delays.get(chat_id, 0)
                    try:
                        spam_msg = random.choice(SPAM_MESSAGES).format(target=target_name)
                        if last_id:
                            sent = await context.bot.send_message(chat_id=chat_id, text=spam_msg, reply_to_message_id=last_id)
                        else:
                            sent = await context.bot.send_message(chat_id=chat_id, text=spam_msg)
                        last_id = sent.message_id
                        self.stats["sent"] += 1
                        if delay > 0: await asyncio.sleep(delay)
                    except asyncio.CancelledError: raise
                    except RetryAfter as e: await asyncio.sleep(int(e.retry_after) + 0.05)
                    except Exception: last_id = None; await asyncio.sleep(0.1)
                break
            except asyncio.CancelledError: break
            except Exception: await asyncio.sleep(0.1)

    async def pfp_loop(self, chat_id, context):
        while True:
            try:
                while self.is_running and not GLOBAL_STOP_EVENT.is_set():
                    delay = self.chat_delays.get(chat_id, 0)
                    try:
                        if PRELOADED_IMAGES:
                            buf = random.choice(PRELOADED_IMAGES)
                            await context.bot.set_chat_photo(chat_id=chat_id, photo=buf)
                        self.stats["sent"] += 1
                        await asyncio.sleep(delay + 2.0)
                    except asyncio.CancelledError: raise
                    except RetryAfter as e: await asyncio.sleep(int(e.retry_after) + 0.05)
                    except Exception: await asyncio.sleep(0.5)
                break
            except asyncio.CancelledError: break

    async def reply_loop(self, chat_id, target_name, context):
        while True:
            try:
                while self.is_running and not GLOBAL_STOP_EVENT.is_set():
                    delay = self.chat_delays.get(chat_id, 0)
                    if chat_id in self.pending_replies and self.pending_replies[chat_id]:
                        async with self.get_lock(chat_id):
                            messages_to_reply = self.pending_replies[chat_id].copy()
                            self.pending_replies[chat_id] = []
                        for msg_id in messages_to_reply:
                            try:
                                reply_msg = random.choice(REPLY_MESSAGES).format(target=target_name)
                                await context.bot.send_message(chat_id=chat_id, text=reply_msg, reply_to_message_id=msg_id)
                                self.stats["sent"] += 1
                                if delay > 0: await asyncio.sleep(delay)
                            except asyncio.CancelledError: raise
                            except RetryAfter as e: await asyncio.sleep(int(e.retry_after) + 0.05)
                            except Exception: pass
                    else: await asyncio.sleep(0.02)
                break
            except asyncio.CancelledError: break
            except Exception: await asyncio.sleep(0.1)

    # ------------------ COMMAND HANDLERS ------------------

    async def start(self, update, context):
        if not await self.check_owner(update): return
        help_text = f"""
𓆩 𝐁𝐎𝐓 {self.bot_number} 𓆪 - ⚡ 𝐇𝐘𝐏𝐄𝐑-𝐗 𝐯𝟑.𝟎 (𝐅𝐔𝐒𝐈𝐎𝐍) ⚡

━━━━ 𝐀𝐓𝐓𝐀𝐂𝐊 𝐂𝐎𝐌𝐌𝐀𝐍𝐃𝐒 ━━━━
/nc <name> - Normal NC Loop
/ncbaap <name> - Max Speed Random NC
/godspeed - Extreme NC (Random Names)
/exoncgodspeed - Ultra Mix NC
/spam <target> - Text Spam Loop
/imagespam <target> - Ultra Fast Image Spam
/slidespam <target> - Reply-Chain Spam
/changepfp - Loop Group PFP Change
/reply <target> - Reply to every message
/all <target> - START EVERYTHING!

━━━━ 𝐀𝐔𝐓𝐎𝐌𝐀𝐓𝐈𝐎𝐍 ━━━━
/auto - Reply to message to start auto-reactions
/del <username> - Auto delete user's messages
/stopauto - Stop auto reactions
/stopdel - Stop auto deletions

━━━━ 𝐂𝐎𝐍𝐓𝐑𝐎𝐋 ━━━━
/delay <sec> - Set delay (default: 0)
/threads <1-50> - Set Multi-threads
/stopall - Stop ALL loops in this chat
/status - Live statistics
"""
        await update.message.reply_text(help_text)

    # SPAM COMMANDS
    async def _start_spam_variant(self, update, context, task_dict, loop_func, action_name, mode="text"):
        if not await self.check_owner(update): return
        if update.effective_chat.type not in [ChatType.GROUP, ChatType.SUPERGROUP]: return
        
        target = " ".join(context.args) if context.args else "HYPER-X"
        chat_id = update.effective_chat.id

        async with get_command_lock(chat_id):
            if chat_id in task_dict: await self.safe_cancel_tasks(task_dict[chat_id])
            num_threads = self.chat_threads.get(chat_id, 1)
            tasks = [asyncio.create_task(loop_func(chat_id, target, context, i+1, mode) if mode else loop_func(chat_id, target, context, i+1)) for i in range(num_threads)]
            task_dict[chat_id] = tasks

        await update.message.reply_text(f"[Bot {self.bot_number}] {action_name} STARTED with {num_threads} threads!")

    async def spam_command(self, update, context): await self._start_spam_variant(update, context, self.active_spam_tasks, self.spam_loop, "TEXT SPAM", "text")
    async def imagespam_command(self, update, context): 
        if not PRELOADED_IMAGES: return await update.message.reply_text("❌ Images not preloaded in RAM!")
        await self._start_spam_variant(update, context, self.active_imagespam_tasks, self.spam_loop, "ULTRA IMAGE SPAM", "image")
    async def slidespam_command(self, update, context): await self._start_spam_variant(update, context, self.active_slide_tasks, self.slide_loop, "SLIDE SPAM", None)

    # NC COMMANDS
    async def nc_command(self, update, context): await self._start_spam_variant(update, context, self.active_name_change_tasks, self.name_change_loop, "NC LOOP", "normal")
    async def ncbaap_command(self, update, context): await self._start_spam_variant(update, context, self.active_name_change_tasks, self.name_change_loop, "NC BAAP", "ncbaap")
    async def godspeed_command(self, update, context): await self._start_spam_variant(update, context, self.active_name_change_tasks, self.name_change_loop, "GODSPEED NC", "godspeed")
    async def exoncgodspeed_command(self, update, context): await self._start_spam_variant(update, context, self.active_name_change_tasks, self.name_change_loop, "EXO GODSPEED NC", "exonc")

    # PFP COMMAND
    async def changepfp_command(self, update, context):
        if not await self.check_owner(update): return
        chat_id = update.effective_chat.id
        async with get_command_lock(chat_id):
            if chat_id in self.active_pfp_tasks: self.active_pfp_tasks[chat_id].cancel()
            self.active_pfp_tasks[chat_id] = asyncio.create_task(self.pfp_loop(chat_id, context))
        await update.message.reply_text(f"[Bot {self.bot_number}] PFP CHANGER STARTED!")

    # ALL IN ONE
    async def all_command(self, update, context):
        if not await self.check_owner(update): return
        target = " ".join(context.args) if context.args else "HYPER-X"
        chat_id = update.effective_chat.id
        num_threads = self.chat_threads.get(chat_id, 1)

        async with get_command_lock(chat_id):
            await self.stop_all_command(update, context) # Clear first
            
            # Start everything
            self.active_spam_tasks[chat_id] = [asyncio.create_task(self.spam_loop(chat_id, target, context, i+1, "text")) for i in range(num_threads)]
            self.active_name_change_tasks[chat_id] = [asyncio.create_task(self.name_change_loop(chat_id, target, context, i+1, "ncbaap")) for i in range(num_threads)]
            if PRELOADED_IMAGES:
                self.active_imagespam_tasks[chat_id] = [asyncio.create_task(self.spam_loop(chat_id, target, context, i+1, "image")) for i in range(1)]
                self.active_pfp_tasks[chat_id] = asyncio.create_task(self.pfp_loop(chat_id, context))

        await update.message.reply_text(f"[Bot {self.bot_number}] 🔥 ALL IN ONE ACTIVATED (Spam+NC+Image+PFP) 🔥")

    # AUTO DELETE & REACT
    async def auto_react_cmd(self, update, context):
        if not await self.check_owner(update) or not update.message.reply_to_message: return
        chat_id = update.effective_chat.id
self.auto_react_targets.setdefault(chat_id, set()).add(update.message.reply_to_message.from_user.id)
        await update.message.reply_text(f"[Bot {self.bot_number}] 🤮 Auto-Reaction Active!")

    async def del_user_cmd(self, update, context):
        if not await self.check_owner(update) or not context.args: return
        chat_id = update.effective_chat.id
        target = context.args[0].replace("@", "").lower()
        self.delete_targets.setdefault(chat_id, set()).add(target)
        await update.message.reply_text(f"[Bot {self.bot_number}] 🎯 Auto-delete set for @{target}")

    async def stop_auto(self, update, context):
        if not await self.check_owner(update): return
        self.auto_react_targets.pop(update.effective_chat.id, None)
        await update.message.reply_text("Stopped auto react.")

    async def stop_del(self, update, context):
        if not await self.check_owner(update): return
        self.delete_targets.pop(update.effective_chat.id, None)
        await update.message.reply_text("Stopped auto delete.")

    # BACKGROUND COLLECTOR (Deletes, Reacts, Replies)
    async def message_collector(self, update, context):
        if not update.message or not update.effective_user: return
        chat_id = update.effective_chat.id
        user = update.effective_user

        # Auto Delete
        if chat_id in self.delete_targets and user.username and user.username.lower() in self.delete_targets[chat_id]:
            try: await update.message.delete()
            except: pass

        # Auto React
        if chat_id in self.auto_react_targets and user.id in self.auto_react_targets[chat_id]:
            try: await update.message.set_reaction([ReactionTypeEmoji(emoji=random.choice(VALID_REACTIONS))])
            except: pass

        # Reply Loop trigger
        if chat_id in self.active_reply_targets:
            msg_id = update.message.message_id
            async with self.get_lock(chat_id):
                if chat_id not in self.pending_replies: self.pending_replies[chat_id] = []
                self.pending_replies[chat_id].append(msg_id)

    # UTILS
    async def stop_all_command(self, update, context):
        if not await self.check_owner(update): return
        chat_id = update.effective_chat.id
        
        async with get_command_lock(chat_id):
            for d in [self.active_spam_tasks, self.active_name_change_tasks, self.active_custom_nc_tasks, self.active_imagespam_tasks, self.active_slide_tasks]:
                if chat_id in d: await self.safe_cancel_tasks(d.pop(chat_id))
            for d in [self.active_reply_tasks, self.active_pfp_tasks]:
                if chat_id in d: d[chat_id].cancel(); d.pop(chat_id)
                
            self.active_reply_targets.pop(chat_id, None)
            self.pending_replies.pop(chat_id, None)
            self.delete_targets.pop(chat_id, None)
            self.auto_react_targets.pop(chat_id, None)
            
        await update.message.reply_text(f"[Bot {self.bot_number}] 🛑 ALL TASKS STOPPED!")

    async def set_delay_command(self, update, context):
        if not await self.check_owner(update): return
        try:
            self.chat_delays[update.effective_chat.id] = float(context.args[0])
            await update.message.reply_text(f"Delay set to {context.args[0]}s")
        except: pass

    async def set_threads_command(self, update, context):
        if not await self.check_owner(update): return
        try:
            self.chat_threads[update.effective_chat.id] = max(1, min(50, int(context.args[0])))
            await update.message.reply_text(f"Threads set to {self.chat_threads[update.effective_chat.id]}")
        except: pass

    async def stats_command(self, update, context):
        if not await self.check_owner(update): return
        up = int(time.time() - self.stats["start_time"])
        await update.message.reply_text(f"📊 Stats [Bot {self.bot_number}]\nSent: {self.stats['sent']}\nErrors: {self.stats['errors']}\nUptime: {up}s")


def build_application(token: str, bot_number: int) -> Application:
    bot_instance = HyperBotInstance(bot_number, OWNER_ID)
    app = Application.builder().token(token).build()
    
    # Register Commands
    cmds = {
        "start": bot_instance.start, "help": bot_instance.start,
        "spam": bot_instance.spam_command, "imagespam": bot_instance.imagespam_command, "slidespam": bot_instance.slidespam_command,
        "nc": bot_instance.nc_command, "ncbaap": bot_instance.ncbaap_command, "godspeed": bot_instance.godspeed_command, "exoncgodspeed": bot_instance.exoncgodspeed_command,
        "changepfp": bot_instance.changepfp_command, "all": bot_instance.all_command,
        "auto": bot_instance.auto_react_cmd, "stopauto": bot_instance.stop_auto,
        "del": bot_instance.del_user_cmd, "stopdel": bot_instance.stop_del,
        "reply": bot_instance.reply_command, "stopall": bot_instance.stop_all_command,
        "delay": bot_instance.set_delay_command, "threads": bot_instance.set_threads_command, "status": bot_instance.stats_command
    }
    for cmd, func in cmds.items(): app.add_handler(CommandHandler(cmd, func))
    
    app.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, bot_instance.message_collector))
    return app


async def run_bot(token: str, bot_number: int):
    try:
        app = build_application(token, bot_number)
        await app.initialize()
        await app.start()
        await app.updater.start_polling(drop_pending_updates=True)
        print(f"✅ [Bot {bot_number}] Armed & Ready!")
        while not GLOBAL_STOP_EVENT.is_set(): await asyncio.sleep(1)
        await app.updater.stop(); await app.stop(); await app.shutdown()
    except Exception as e:
        print(f"❌ [Bot {bot_number}] Error: {e}")

async def main():
    print("=" * 60)
    print("⚡ HYPER-X v3.0 (FUSION EDITION) - STARTING ⚡")
    print("=" * 60)
    
    preload_images(50) # Load fast images into RAM
    
    def signal_handler(sig, frame):
        print("\n🛑 Shutdown signal received...")
        GLOBAL_STOP_EVENT.set()
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    tasks = [asyncio.create_task(run_bot(token, i)) for i, token in enumerate(BOT_TOKENS, 1)]
    
    print(f"\n🚀 Booting {len(BOT_TOKENS)} bots with multi-threading support...")
    try:
        await asyncio.gather(*tasks, return_exceptions=True)
    finally:
        GLOBAL_STOP_EVENT.set()
        for bot in ALL_BOT_INSTANCES.values(): await bot.stop_all_tasks_globally()

if __name__ == "__main__":
    asyncio.run(main())
          print(f"⏳ Pre-loading {count} images for ultra-fast spam...")
    try:
        from PIL import Image
        for _ in range(count):
            color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
            img = Image.new("RGB", (200, 200), color)
            buf = io.BytesIO()
            img.save(buf, format="JPEG")
            PRELOADED_IMAGES.append(buf.getvalue())
        print(f"✅ {len(PRELOADED_IMAGES)} Images loaded into RAM successfully!")
    except Exception as e:
        print(f"❌ Failed to preload images (PIL not installed?): {e}")

ALL_BOT_INSTANCES: Dict[int, 'HyperBotInstance'] = {}
GLOBAL_STOP_EVENT = asyncio.Event()
COMMAND_LOCKS: Dict[int, asyncio.Lock] = {}

def get_command_lock(chat_id: int) -> asyncio.Lock:
    if chat_id not in COMMAND_LOCKS:
        COMMAND_LOCKS[chat_id] = asyncio.Lock()
    return COMMAND_LOCKS[chat_id]

class HyperBotInstance:
    def __init__(self, bot_number, owner_id):
        self.bot_number = bot_number
        self.owner_id = owner_id
        self.authorized_users = set(DEFAULT_AUTHORIZED_USERS)
        
        # TASK TRACKERS
        self.active_spam_tasks: Dict[int, List[asyncio.Task]] = {}
        self.active_name_change_tasks: Dict[int, List[asyncio.Task]] = {}
        self.active_custom_nc_tasks: Dict[int, List[asyncio.Task]] = {}
        self.active_reply_tasks: Dict[int, asyncio.Task] = {}
        self.active_imagespam_tasks: Dict[int, List[asyncio.Task]] = {}
        self.active_slide_tasks: Dict[int, List[asyncio.Task]] = {}
        self.active_pfp_tasks: Dict[int, asyncio.Task] = {}
        
        # TARGET TRACKERS
        self.active_reply_targets: Dict[int, str] = {}
        self.pending_replies: Dict[int, List[int]] = {}
        self.delete_targets: Dict[int, Set[str]] = {}
        self.auto_react_targets: Dict[int, Set[int]] = {}
        
        self.chat_delays: Dict[int, float] = {}
        self.chat_threads: Dict[int, int] = {}
        self.locks: Dict[int, asyncio.Lock] = {}
        self.stats = {"sent": 0, "errors": 0, "start_time": time.time()}
        self.is_running = True
        ALL_BOT_INSTANCES[bot_number] = self

    def get_lock(self, chat_id):
        if chat_id not in self.locks:
            self.locks[chat_id] = asyncio.Lock()
        return self.locks[chat_id]

    async def check_owner(self, update):
        user_id = update.effective_user.id
        if not (user_id == self.owner_id or user_id in self.authorized_users):
            return False
        return True

    async def check_main_owner(self, update):
        if update.effective_user.id != self.owner_id:
            return False
        return True

    async def safe_cancel_tasks(self, tasks: List[asyncio.Task]):
        for task in tasks:
            if not task.done(): task.cancel()
        for task in tasks:
            try: await asyncio.wait_for(asyncio.shield(task), timeout=2.0)
            except: pass

    async def stop_all_tasks_globally(self):
        all_tasks = []
        for d in [self.active_spam_tasks, self.active_name_change_tasks, self.active_custom_nc_tasks, 
                  self.active_imagespam_tasks, self.active_slide_tasks]:
            for tasks in list(d.values()): all_tasks.extend(tasks)
            d.clear()
            
        for d in [self.active_reply_tasks, self.active_pfp_tasks]:
            for task in list(d.values()): all_tasks.append(task)
            d.clear()
            
        self.active_reply_targets.clear()
        self.pending_replies.clear()
        
        await self.safe_cancel_tasks(all_tasks)
        return len(all_tasks)

    # ------------------ LOOP ENGINES ------------------

    async def name_change_loop(self, chat_id, base_name, context, worker_id=1, mode="normal"):
        msg_index = 0
        while True:
            try:
                while self.is_running and not GLOBAL_STOP_EVENT.is_set():
                    delay = self.chat_delays.get(chat_id, 0)
                    try:
                        if mode == "godspeed":
                            display_name = random.choice(GODSPEED_NAMES)
                        elif mode == "exonc":
                            display_name = f"{random.choice(GODSPEED_NAMES)} {random.choice(NAME_CHANGE_MESSAGES).split()[0]}"[:255]
                        elif mode == "ncbaap":
                            display_name = random.choice(NAME_CHANGE_MESSAGES).format(target=base_name)[:255]
                        else:
                            current_msg = NAME_CHANGE_MESSAGES[msg_index % len(NAME_CHANGE_MESSAGES)]
                            display_name = current_msg.format(target=base_name)[:255]

                        await context.bot.set_chat_title(chat_id=chat_id, title=display_name)
                        msg_index += 1
                        self.stats["sent"] += 1
                        if delay > 0: await asyncio.sleep(delay)
                    except asyncio.CancelledError: raise
                    except RetryAfter as e: await asyncio.sleep(int(e.retry_after) + 0.05)
                    except (TimedOut, NetworkError): pass
                    except (BadRequest, Forbidden): await asyncio.sleep(0.1); msg_index += 1
                    except Exception: self.stats["errors"] += 1; msg_index += 1
                break
            except asyncio.CancelledError: break
            except Exception: await asyncio.sleep(0.1)

    async def spam_loop(self, chat_id, target_name, context, worker_id, mode="text"):
        while True:
            try:
                while self.is_running and not GLOBAL_STOP_EVENT.is_set():
                    delay = self.chat_delays.get(chat_id, 0)
                    try:
                        if mode == "image" and PRELOADED_IMAGES:
                            img_bytes = random.choice(PRELOADED_IMAGES)
                            await context.bot.send_photo(chat_id=chat_id, photo=img_bytes, caption=f"⚡ HYPER-X SPAM #{random.randint(1,999)}")
                        else:
                            spam_msg = random.choice(SPAM_MESSAGES).format(target=target_name)
                            await context.bot.send_message(chat_id=chat_id, text=spam_msg)
                            
                        self.stats["sent"] += 1
                        if delay > 0: await asyncio.sleep(delay)
                    except asyncio.CancelledError: raise
                    except RetryAfter as e: await asyncio.sleep(int(e.retry_after) + 0.05)
                    except (TimedOut, NetworkError): pass
                    except (BadRequest, Forbidden): await asyncio.sleep(0.1)
                    except Exception: self.stats["errors"] += 1
                break
            except asyncio.CancelledError: break
            except Exception: await asyncio.sleep(0.1)

    async def slide_loop(self, chat_id, target_name, context, worker_id):
        last_id = None
        while True:
            try:
                while self.is_running and not GLOBAL_STOP_EVENT.is_set():
                    delay = self.chat_delays.get(chat_id, 0)
                    try:
                        spam_msg = random.choice(SPAM_MESSAGES).format(target=target_name)
                        if last_id:
                            sent = await context.bot.send_message(chat_id=chat_id, text=spam_msg, reply_to_message_id=last_id)
                        else:
                            sent = await context.bot.send_message(chat_id=chat_id, text=spam_msg)
                        last_id = sent.message_id
                        self.stats["sent"] += 1
                        if delay > 0: await asyncio.sleep(delay)
                    except asyncio.CancelledError: raise
                    except RetryAfter as e: await asyncio.sleep(int(e.retry_after) + 0.05)
                    except Exception: last_id = None; await asyncio.sleep(0.1)
                break
            except asyncio.CancelledError: break
            except Exception: await asyncio.sleep(0.1)

    async def pfp_loop(self, chat_id, context):
        while True:
            try:
                while self.is_running and not GLOBAL_STOP_EVENT.is_set():
                    delay = self.chat_delays.get(chat_id, 0)
                    try:
                        if PRELOADED_IMAGES:
                            buf = random.choice(PRELOADED_IMAGES)
                            await context.bot.set_chat_photo(chat_id=chat_id, photo=buf)
                        self.stats["sent"] += 1
                        await asyncio.sleep(delay + 2.0)
                    except asyncio.CancelledError: raise
                    except RetryAfter as e: await asyncio.sleep(int(e.retry_after) + 0.05)
                    except Exception: await asyncio.sleep(0.5)
                break
            except asyncio.CancelledError: break

    async def reply_loop(self, chat_id, target_name, context):
        while True:
            try:
                while self.is_running and not GLOBAL_STOP_EVENT.is_set():
                    delay = self.chat_delays.get(chat_id, 0)
                    if chat_id in self.pending_replies and self.pending_replies[chat_id]:
                        async with self.get_lock(chat_id):
                            messages_to_reply = self.pending_replies[chat_id].copy()
                            self.pending_replies[chat_id] = []
                        for msg_id in messages_to_reply:
                            try:
                                reply_msg = random.choice(REPLY_MESSAGES).format(target=target_name)
                                await context.bot.send_message(chat_id=chat_id, text=reply_msg, reply_to_message_id=msg_id)
                                self.stats["sent"] += 1
                                if delay > 0: await asyncio.sleep(delay)
                            except asyncio.CancelledError: raise
                            except RetryAfter as e: await asyncio.sleep(int(e.retry_after) + 0.05)
                            except Exception: pass
                    else: await asyncio.sleep(0.02)
                break
            except asyncio.CancelledError: break
            except Exception: await asyncio.sleep(0.1)

    # ------------------ COMMAND HANDLERS ------------------

    async def start(self, update, context):
        if not await self.check_owner(update): return
        help_text = f"""
𓆩 𝐁𝐎𝐓 {self.bot_number} 𓆪 - ⚡ 𝐇𝐘𝐏𝐄𝐑-𝐗 𝐯𝟑.𝟎 (𝐅𝐔𝐒𝐈𝐎𝐍) ⚡

━━━━ 𝐀𝐓𝐓𝐀𝐂𝐊 𝐂𝐎𝐌𝐌𝐀𝐍𝐃𝐒 ━━━━
/nc <name> - Normal NC Loop
/ncbaap <name> - Max Speed Random NC
/godspeed - Extreme NC (Random Names)
/exoncgodspeed - Ultra Mix NC
/spam <target> - Text Spam Loop
/imagespam <target> - Ultra Fast Image Spam
/slidespam <target> - Reply-Chain Spam
/changepfp - Loop Group PFP Change
/reply <target> - Reply to every message
/all <target> - START EVERYTHING!

━━━━ 𝐀𝐔𝐓𝐎𝐌𝐀𝐓𝐈𝐎𝐍 ━━━━
/auto - Reply to message to start auto-reactions
/del <username> - Auto delete user's messages
/stopauto - Stop auto reactions
/stopdel - Stop auto deletions

━━━━ 𝐂𝐎𝐍𝐓𝐑𝐎𝐋 ━━━━
/delay <sec> - Set delay (default: 0)
/threads <1-50> - Set Multi-threads
/stopall - Stop ALL loops in this chat
/status - Live statistics
"""
        await update.message.reply_text(help_text)

    # SPAM COMMANDS
    async def _start_spam_variant(self, update, context, task_dict, loop_func, action_name, mode="text"):
        if not await self.check_owner(update): return
        if update.effective_chat.type not in [ChatType.GROUP, ChatType.SUPERGROUP]: return
        
        target = " ".join(context.args) if context.args else "HYPER-X"
        chat_id = update.effective_chat.id

        async with get_command_lock(chat_id):
            if chat_id in task_dict: await self.safe_cancel_tasks(task_dict[chat_id])
            num_threads = self.chat_threads.get(chat_id, 1)
            tasks = [asyncio.create_task(loop_func(chat_id, target, context, i+1, mode) if mode else loop_func(chat_id, target, context, i+1)) for i in range(num_threads)]
            task_dict[chat_id] = tasks

        await update.message.reply_text(f"[Bot {self.bot_number}] {action_name} STARTED with {num_threads} threads!")

    async def spam_command(self, update, context): await self._start_spam_variant(update, context, self.active_spam_tasks, self.spam_loop, "TEXT SPAM", "text")
    async def imagespam_command(self, update, context): 
        if not PRELOADED_IMAGES: return await update.message.reply_text("❌ Images not preloaded in RAM!")
        await self._start_spam_variant(update, context, self.active_imagespam_tasks, self.spam_loop, "ULTRA IMAGE SPAM", "image")
    async def slidespam_command(self, update, context): await self._start_spam_variant(update, context, self.active_slide_tasks, self.slide_loop, "SLIDE SPAM", None)

    # NC COMMANDS
    async def nc_command(self, update, context): await self._start_spam_variant(update, context, self.active_name_change_tasks, self.name_change_loop, "NC LOOP", "normal")
    async def ncbaap_command(self, update, context): await self._start_spam_variant(update, context, self.active_name_change_tasks, self.name_change_loop, "NC BAAP", "ncbaap")
    async def godspeed_command(self, update, context): await self._start_spam_variant(update, context, self.active_name_change_tasks, self.name_change_loop, "GODSPEED NC", "godspeed")
    async def exoncgodspeed_command(self, update, context): await self._start_spam_variant(update, context, self.active_name_change_tasks, self.name_change_loop, "EXO GODSPEED NC", "exonc")

    # PFP COMMAND
    async def changepfp_command(self, update, context):
        if not await self.check_owner(update): return
        chat_id = update.effective_chat.id
        async with get_command_lock(chat_id):
            if chat_id in self.active_pfp_tasks: self.active_pfp_tasks[chat_id].cancel()
            self.active_pfp_tasks[chat_id] = asyncio.create_task(self.pfp_loop(chat_id, context))
        await update.message.reply_text(f"[Bot {self.bot_number}] PFP CHANGER STARTED!")

    # ALL IN ONE
    async def all_command(self, update, context):
        if not await self.check_owner(update): return
        target = " ".join(context.args) if context.args else "HYPER-X"
        chat_id = update.effective_chat.id
        num_threads = self.chat_threads.get(chat_id, 1)

        async with get_command_lock(chat_id):
            await self.stop_all_command(update, context) # Clear first
            
            # Start everything
            self.active_spam_tasks[chat_id] = [asyncio.create_task(self.spam_loop(chat_id, target, context, i+1, "text")) for i in range(num_threads)]
            self.active_name_change_tasks[chat_id] = [asyncio.create_task(self.name_change_loop(chat_id, target, context, i+1, "ncbaap")) for i in range(num_threads)]
            if PRELOADED_IMAGES:
                self.active_imagespam_tasks[chat_id] = [asyncio.create_task(self.spam_loop(chat_id, target, context, i+1, "image")) for i in range(1)]
                self.active_pfp_tasks[chat_id] = asyncio.create_task(self.pfp_loop(chat_id, context))

        await update.message.reply_text(f"[Bot {self.bot_number}] 🔥 ALL IN ONE ACTIVATED (Spam+NC+Image+PFP) 🔥")

    # AUTO DELETE & REACT
    async def auto_react_cmd(self, update, context):
        if not await self.check_owner(update) or not update.message.reply_to_message: return
        chat_id = update.effective_chat.id
      
