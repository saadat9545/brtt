# -*- coding: utf-8 -*-
from datetime import timedelta
from pickle import dump
from pyrogram import filters, enums, Client, errors
from pyrogram.types import Message, ChatPermissions
from utils.filters import check
from utils.clients import ApiClient
from utils.config import SETTINGS, SUDO, LINKS, Clients 
from pickle import dump
from utils import Buttons
import string, random as rnd, shutil, time as myTime, re, os, sys, pyrogram
from os import remove as os_remove
import sqlite3
import jdatetime as jdf
from data.database import db

#------------------------------------------------------


#-----------------------------------------------------
def save_settings():
    with open('settings.pkl', 'wb') as f:
        dump(SETTINGS, f)
#-----------------------------------------------------





@ApiClient.on_message(filters.private  & filters.command('start'))
async def Start_Bot(bot: Client, msg: Message):
    user_id = msg.from_user.id
    name = msg.from_user.mention
    user_fullname = msg.from_user.first_name
    username = msg.from_user.username
    Date = jdf.date.today().strftime("%Y/%m/%d")
    start_parametr = msg.command[1] if len(msg.command) > 1 else None
    text = (f'✦ به اولین و پیشرفته‌ترین ربات فرم‌دهی‌ نتیجه دقیق در تلگرام خوش آمدید 🤖n'
            f'✦ برای استفاده از ربات، لطفا گزینه مورد نظر خود را انتخاب کنید 👇🏻')


    try:
        if user_id in SUDO or user_id in db.admin_User_id(user_id):
            await msg.reply_text(f'سلام مدیر 💎\n🔧 از منوی زیر میتونید ربات را کنترل کنید 🔧', 
            reply_markup = Buttons.Management)
        
    except:
            if start_parametr:
                try:
                    target = await bot.get_chat(int(msg.command[1]))

                    if not db.User_id(user_id):
                        db.Add_User(user_fullname, user_id, username,0,Date)
                        db.update_data(int(msg.command[1]))

                        tx = (f'◈ کاربر {name}\n'
                            f'◈ از طرف لینک اختصاصی شما وارد ربات شد !\n'
                            f' ◂ توجه داشته باشید افرادی که دعوت میکنید حتما باید بت باز باشن در غیر این صورت چیزی نمیگیرید\n'
                            f'◂ میتونید لینکتون رو به رفیقای بت بازتون یا ممبرای سایر گپای بت ارسال کنید\n'
                            f'┈┅┅━━━━━━✦━━━━━━┅┅┈\n'
                            f"❇️ تعداد افراد دعوت شده توسط شما : {db.select_invited(int(msg.command[1]))}")

                        await bot.send_message(int(msg.command[1]), tx)
                        for sudo in SUDO:
                            await bot.send_message(sudo, f'◈ کـاربر : {name}\n'
                                                        f'◂ آیدی : {user_id}\n'
                                                        f' توسط لینک اختصاصیه : {target.first_name}\n'
                                                        f'عضو ربات شد 🎉\n'
                                                        f'┈┅┅━━━━━━✦━━━━━━┅┅┈\n'
                                                        f"تعداد افراد دعوت کرده : {db.select_invited(int(msg.command[1]))}")
                except:
                    if not db.User_id(user_id):
                        db.Add_User(user_fullname, user_id, username,0,Date)

            else:
                if not db.User_id(user_id):
                    db.Add_User(user_fullname, user_id, username,0,Date)
                    for sudo in SUDO:
                        await bot.send_message(sudo, f'◈ کـاربر {name}\n ◂ آیدی : {user_id}\nعضو ربات شد 🎉')
            
            await msg.reply_text(text, 
            reply_markup = Buttons.Start)
    db.update_last_seen(msg.from_user.id)


@ApiClient.on_message(filters.private & filters.regex('💰 زیرمجموعه گیری و کسب درآمد 💰$') & check)
async def Substance(_, msg: Message):
    await msg.reply_text(f'گزینه مورد نظر خود را انتخاب کنید 👇🏻',
    reply_markup = Buttons.Link_bot)
    db.update_last_seen(msg.from_user.id)

@ApiClient.on_message(filters.private & filters.regex('حساب من👤$') & check )
async def Get_Substance_info(_, msg: Message):
    a = db.User_information(msg.from_user.id)
    await msg.reply(a)
    db.update_last_seen(msg.from_user.id)

                        
@ApiClient.on_message(filters.private & filters.regex('🔗 لینک اختصاصی$'))
async def Get_Substance_link(bot: Client, msg: Message):
    tex_bn = await bot.get_messages(msg.chat.id, SETTINGS['text_baner'])
    link = f'https://telegram.me/tipcorrect_bot?start={msg.from_user.id}'
    text = tex_bn.text.replace('LINK',link)
    text2 = (f'👆🏻 لینک اختتصاصی شما\n'
             f'✦ میتونید با بنر بالا یا‌ کپی لینک و روش دلخواه خود اقدام به جذب کاربر کنید\n'
             f'بعد از دعوت 20 کاربر بت‌باز‌ برای دریافت ووچر به آیدی زیر پیام بدید 👇🏻\n'
             f'🆔 t.me/omid_tip\n🆔 t.me/omid_tip\n'
             f'⚠️ اعضایی که میارید حتما باید بت‌باز باشن وگرنه چیزی بهتون تعلق نمیگیره')
    try:
        banner = await bot.get_messages(msg.chat.id, SETTINGS['link_baner'])
        b = await banner.copy(msg.chat.id, caption = text)
        
        await bot.send_message(msg.chat.id, text2 , reply_to_message_id = b.id)
    except:
        b = await msg.reply_text(text)
        await bot.send_message(msg.chat.id, text2 , reply_to_message_id = b.id)
    db.update_last_seen(msg.from_user.id)


        
@ApiClient.on_message(filters.private & filters.regex('🟢 سایت مورد تایید جهت شرطبندی 🟢') & check) 
async def site_baner(bot: Client, msg: Message):
    try:
        banner = await bot.get_messages(msg.chat.id, SETTINGS['link_site'])
        await banner.copy(msg.chat.id, reply_markup = Buttons.Site_link)
    except:
        await msg.reply_text(f'<b><i>سایتی تنظیم نشده است !</i></b>',
        reply_markup = Buttons.Site_link)
    db.update_last_seen(msg.from_user.id)

@ApiClient.on_message(filters.private & filters.regex('🔗 آدرس بدون فیلتر‌ 🔗') & check)
async def bet_site_link(bot: Client, msg: Message):
    try:
        banner = await bot.get_messages(msg.chat.id, SETTINGS['no_fillter'])
        await banner.copy(msg.chat.id, reply_markup = Buttons.back_Bot)
    except:
        await msg.reply_text(f'<b><i>لینکی تنظیم نشده است !</i></b>')
    db.update_last_seen(msg.from_user.id)

@ApiClient.on_message(filters.private & filters.regex('💬 ارتباط با پشتیبانی 💬$') & check)
async def Support(_, msg: Message):
    await msg.reply_text(f'🗣 برای ارتباط با پشتیبانی، از دکمه زیر استفاده کنید :',
    reply_markup=Buttons.Support('omid_tip'))
    db.update_last_seen(msg.from_user.id)

@ApiClient.on_message(filters.private & filters.regex('🔄 بازگشت 🔄$') & check)
async def back_start(_, msg: Message):

    text = (f'✦ به پیشرفته‌ترین و متفاوت‌ترین ربات فرم‌دهی‌ در تلگرام خوش آمدید 🤖\n'
            f'✦ برای استفاده از ربات، لطفا گزینه مورد نظر خود را انتخاب کنی')

    await msg.reply_text(text, reply_markup = Buttons.Start)
    db.update_last_seen(msg.from_user.id)



@ApiClient.on_message(filters.private & filters.regex('🤖 سایر ربات‌های ما 🤖$') & check)
async def send_ourbots_form(bot: Client, msg: Message):
    try:
        banner = await bot.get_messages(msg.chat.id, SETTINGS['ourbots'])
        await banner.copy(msg.chat.id)
    except:
        await msg.reply_text(f'<b><i>رباتی تنظیم نشده است !</i></b>')
    db.update_last_seen(msg.from_user.id)


@ApiClient.on_message(filters.private & filters.regex('💥 دریافت فرم رایگان 💥$') & check)
async def Get_Bet_Form(_, msg: Message):
    await msg.reply_text(f'<b>لطفا فرم مورد نظر خودتون رو انتخاب کنید 👇🏻</b>', 
    reply_markup = Buttons.bet_form)
    db.update_last_seen(msg.from_user.id)


@ApiClient.on_message(filters.private & filters.regex('💯 شوربت | شرطبندی بدون باخت 💯$') & check)
async def send_vip_form(bot: Client, msg: Message):
    try:
        banner = await bot.get_messages(msg.chat.id, SETTINGS['vip_form'])
        await banner.copy(msg.chat.id)
    except:
        await msg.reply_text(f'<b><i>فرمی تنظیم نشده است !</i></b>')
    db.update_last_seen(msg.from_user.id)


@ApiClient.on_message(filters.private & filters.regex('⚽️ نتیجه دقیق برای آپشن گیری‌ ⚽️$') & check)
async def send_footbal_form(bot: Client, msg: Message):
    try:
        banner = await bot.get_messages(msg.chat.id, SETTINGS['footbal_form'])
        await banner.copy(msg.chat.id)
    except:
        await msg.reply_text(f'<b><i>فرمی تنظیم نشده است !</i></b>')
    db.update_last_seen(msg.from_user.id)

# @ApiClient.on_message(filters.private & filters.regex('🏀 فـرم بـسـکـتـبـال 🏀$') & check)
# async def send_basketball_form(bot: Client, msg: Message):
#     try:
#         banner = await bot.get_messages(msg.chat.id, SETTINGS['basket_form'])
#         await banner.copy(msg.chat.id)
#     except:
#         await msg.reply_text(f'<b><i>فرمی تنظیم نشده است !</i></b>')
#     db.update_last_seen(msg.from_user.id)


@ApiClient.on_message(filters.private & filters.regex('پنل اصلی ⚙️$'))
async def sudo_panel(bot: Client, msg: Message):
    text = (f'✦ به پیشرفته‌ترین و متفاوت‌ترین ربات فرم‌دهی‌ در تلگرام خوش آمدید 🤖\n'
=            f'✦ برای استفاده از ربات، لطفا گزینه مورد نظر خود را انتخاب کنی')

    await msg.reply_text(text, reply_markup = Buttons.Start)

