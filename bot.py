from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters, ConversationHandler

# Define states for the conversation
LANGUAGE, CHOICE, UNIVERSITY, STAGE, BLOCK, FAQ = range(6)

# Define the language selection keyboard
language_keyboard = [['کوردی', 'English']]
language_markup = ReplyKeyboardMarkup(language_keyboard, one_time_keyboard=True)

# Define the choice keyboard after language selection
choice_keyboard_english = [['FAQ', 'Services'], ['Go Back']]
choice_keyboard_kurdish = [['پرسەیەکان', 'خزمەتگوزاریەکان'], ['گەرانەوە']]

# Define the FAQ keyboard with questions
faq_keyboard_english = [['What is Zankys?', 'How do I access a Zankys Package deal?'], 
                        ['How can I pay?', 'Is there a refund?'], 
                        ['Is there repercussions if someone leaks the package?', 'How is the quality of the Zankys products?'], 
                        ['Go Back']]

faq_keyboard_kurdish = [['زانکیس چییە؟', 'چۆن دەتوانم دەستگەیشتن بە مامەڵەی پاکێجی زانکیس بکەم؟'],
                        ['چۆن دەتوانم پارە بدەم؟', 'ئایا پارە دەگەڕێتەوە؟'],
                        ['ئایا کاردانەوەی هەیە ئەگەر کەسێک پاکەتەکە بۆ کەسێکی تر دزەبکات؟', 'کوالیتی بەرهەمەکانی زانکیس چۆنە؟'], 
                        ['گەرانەوە']]

# Define the university selection keyboards
hmu_keyboard_kurdish = [['Stage 1', 'Stage 2', 'Stage 3', 'Stage 4'], ['گەرانەوە']]
ukh_keyboard_kurdish = [['Stage 3'], ['گەرانەوە']]
university_keyboard_kurdish = [['HMU', 'UKH'], ['گەرانەوە']]

hmu_keyboard_english = [['Stage 1', 'Stage 2', 'Stage 3', 'Stage 4'], ['Go Back']]
ukh_keyboard_english = [['Stage 3'], ['Go Back']]
university_keyboard_english = [['HMU', 'UKH'], ['Go Back']]

# Define block options for each stage
stage1_blocks = [['Block 1', 'Block 2'], ['Go Back']]
stage2_blocks = [['IBS Block', 'MSD Block', 'HP Block', 'CVS Block', 'RS Block'], ['Go Back']]
stage3_blocks = [['GIT Block', 'GUE Block', 'NS Block', 'Transitional Block'], ['Go Back']]
stage4_blocks = [['Medicine Block', 'Surgery Block', 'OBGY Block', 'CM + BS Block'], ['Go Back']]  # Added Stage 4 options

# Answers for FAQs
faq_answers_english = {
    'What is Zankys?': "Zankys is an education company that currently specializes in Medicine that focuses on making resources to help out students. We are the number 1 student-based organization that offers help for students and is not affiliated with any governmental or political party.",
    'How do I access a Zankys Package deal?': "You message the Zankys bot, choose your language then click on services, then your university, then your stage, then the specific package you want. The bot will send a message to the Zankys team to contact you.",
    'How can I pay?': "We accept FIB, Fastpay, Naswallet, Zaincash, Qi Card, and also PTP (person-to-person payment).",
    'Is there a refund?': "No, after you sign the deal that you bought the package, we do not offer any refunds.",
    'Is there repercussions if someone leaks the package?': "Yes, you will get blacklisted from being offered any other Zankys deal in the future and kicked from all the Zankys channels and perks Zankys offer.",
    'How is the quality of the Zankys products?': "Top of line quality, made by using the ZanAI with 2 years’ experience with 5 branches in 2 different universities."
}

faq_answers_kurdish = {
    'زانکیس چییە؟': "زانکیس کۆمپانیایەکی پەروەردەییە کە لە ئێستادا پسپۆڕە لە پزیشکی کە تەرکیز لەسەر دروستکردنی پەناگە بۆ یارمەتیدانی قوتابیان دەکات. ئێمە ژمارە 1 ڕێکخراوی خوێندکارین کە یارمەتی بۆ قوتابیان پێشکەش دەکەین و سەر بە هیچ حکومەت و پارتێکی سیاسی نین.",
    'چۆن دەتوانم دەستگەیشتن بە مامەڵەی پاکێجی زانکیس بکەم؟': "تۆ پەیام بۆ بۆتی زانکیس دەنێریت، زمانی خۆت هەڵدەبژێریت پاشان کرتە لەسەر خزمەتگوزاریەکان دەکەیت پاشان زانکۆکەت پاشان قۆناغەکەت پاشان ئەو پاکێجە تایبەتەی کە دەتەوێت. بۆتەکە نامەیەک دەنێرێت بۆ تیمی زانکیس بۆ ئەوەی پەیوەندیت پێوە بکات.",
    'چۆن دەتوانم پارە بدەم؟': "ئێمە FIB، Fastpay، Naswallet، Zaincash، Qi Card و هەروەها PTP (پارەدانی کەسی بۆ کەس) قبوڵ دەکەین.",
    'ئایا پارە دەگەڕێتەوە؟': "نەخێر، دوای ئەوەی گرێبەستەکەت واژۆ کرد کە پاکێجەکەت کڕیوە، ئێمە هیچ پارەیەک نادەینەوە.",
    'ئایا کاردانەوەی هەیە ئەگەر کەسێک پاکەتەکە بۆ کەسێکی تر دزەبکات؟': "بەڵێ، تۆ دەخرێنە لیستی ڕەشەوە لە هەر مامەڵەیەکی تری زانکیس لە داهاتوودا، و لە هەموو کەناڵەکانی زانکیس دەردەکرێیت و ئەو ئیمتیازاتانەی زانکیس پێشکەشی دەکات.",
    'کوالیتی بەرهەمەکانی زانکیس چۆنە؟': "کوالیتی بەرز، بە بەکارهێنانی ZanAI لەگەڵ 2 ساڵ ئەزموون لەگەڵ 5 لق لە 2 زانکۆی جیاواز دروستکراوە."
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # Welcome message and language selection
    await update.message.reply_text(
        'Hello! Welcome to Zankys. Please select your language\n'
        'سڵاو! بەخێربێن بۆ زانکیس. تکایە زمانەکەت هەڵبژێرە',
        reply_markup=language_markup
    )
    return LANGUAGE

async def handle_language(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # Handle language choice
    user_language = update.message.text
    context.user_data['language'] = user_language  # Store the selected language

    if user_language == 'English':
        await update.message.reply_text('Please choose an option:', reply_markup=ReplyKeyboardMarkup(choice_keyboard_english, one_time_keyboard=True))
        return CHOICE
    elif user_language == 'کوردی':
        await update.message.reply_text('تکایە یەکێک هەڵبژێرە:', reply_markup=ReplyKeyboardMarkup(choice_keyboard_kurdish, one_time_keyboard=True))
        return CHOICE
    else:
        await update.message.reply_text('Please choose a valid option', reply_markup=language_markup)
        return LANGUAGE

async def handle_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # Handle choice after language selection
    user_choice = update.message.text
    language = context.user_data.get('language')

    if language == 'English':
        if user_choice == 'FAQ':
            await update.message.reply_text('Here are some FAQs:', reply_markup=ReplyKeyboardMarkup(faq_keyboard_english, one_time_keyboard=True))
            return FAQ
        elif user_choice == 'Services':
            await update.message.reply_text('Choose your University', reply_markup=ReplyKeyboardMarkup(university_keyboard_english, one_time_keyboard=True))
            return UNIVERSITY
        elif user_choice == 'Go Back':
            return await handle_language(update, context)
        else:
            await update.message.reply_text('Please choose a valid option', reply_markup=ReplyKeyboardMarkup(choice_keyboard_english, one_time_keyboard=True))
            return CHOICE

    elif language == 'کوردی':
        if user_choice == 'پرسەیەکان':
            await update.message.reply_text('ئەمانە پرسەیەکانن:', reply_markup=ReplyKeyboardMarkup(faq_keyboard_kurdish, one_time_keyboard=True))
            return FAQ
        elif user_choice == 'خزمەتگوزاریەکان':
            await update.message.reply_text('زانکۆیەکە هەڵبژێرە', reply_markup=ReplyKeyboardMarkup(university_keyboard_kurdish, one_time_keyboard=True))
            return UNIVERSITY
        elif user_choice == 'گەرانەوە':
            return await handle_language(update, context)
        else:
            await update.message.reply_text('تکایە هەڵبژاردەیەکی دروست هەڵبژێرە', reply_markup=ReplyKeyboardMarkup(choice_keyboard_kurdish, one_time_keyboard=True))
            return CHOICE

async def handle_faq(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # Handle FAQ choice
    user_choice = update.message.text
    language = context.user_data.get('language')

    if language == 'English':
        if user_choice in faq_answers_english:
            await update.message.reply_text(faq_answers_english[user_choice], reply_markup=ReplyKeyboardMarkup(faq_keyboard_english, one_time_keyboard=True))
            return FAQ
        elif user_choice == 'Go Back':
            return await handle_choice(update, context)
        else:
            await update.message.reply_text('Please choose a valid question', reply_markup=ReplyKeyboardMarkup(faq_keyboard_english, one_time_keyboard=True))
            return FAQ

    elif language == 'کوردی':
        if user_choice in faq_answers_kurdish:
            await update.message.reply_text(faq_answers_kurdish[user_choice], reply_markup=ReplyKeyboardMarkup(faq_keyboard_kurdish, one_time_keyboard=True))
            return FAQ
        elif user_choice == 'گەرانەوە':
            return await handle_choice(update, context)
        else:
            await update.message.reply_text('تکایە پرسیارێکی دروست هەڵبژێرە', reply_markup=ReplyKeyboardMarkup(faq_keyboard_kurdish, one_time_keyboard=True))
            return FAQ

async def handle_university(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # Handle university choice
    user_choice = update.message.text
    language = context.user_data.get('language')

    if language == 'English':
        if user_choice == 'HMU':
            await update.message.reply_text('Choose your stage', reply_markup=ReplyKeyboardMarkup(hmu_keyboard_english, one_time_keyboard=True))
            return STAGE
        elif user_choice == 'UKH':
            await update.message.reply_text('Choose your stage', reply_markup=ReplyKeyboardMarkup(ukh_keyboard_english, one_time_keyboard=True))
            return STAGE
        elif user_choice == 'Go Back':
            return await handle_choice(update, context)
        else:
            await update.message.reply_text('Please choose a valid university', reply_markup=ReplyKeyboardMarkup(university_keyboard_english, one_time_keyboard=True))
            return UNIVERSITY

    elif language == 'کوردی':
        if user_choice == 'HMU':
            await update.message.reply_text('پۆلت هەڵبژێرە', reply_markup=ReplyKeyboardMarkup(hmu_keyboard_kurdish, one_time_keyboard=True))
            return STAGE
        elif user_choice == 'UKH':
            await update.message.reply_text('پۆلت هەڵبژێرە', reply_markup=ReplyKeyboardMarkup(ukh_keyboard_kurdish, one_time_keyboard=True))
            return STAGE
        elif user_choice == 'گەرانەوە':
            return await handle_choice(update, context)
        else:
            await update.message.reply_text('تکایە زانکۆیەکی دروست هەڵبژێرە', reply_markup=ReplyKeyboardMarkup(university_keyboard_kurdish, one_time_keyboard=True))
            return UNIVERSITY

async def handle_stage(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # Handle stage choice
    user_choice = update.message.text
    language = context.user_data.get('language')

    if user_choice == 'Stage 1':
        await update.message.reply_text('Choose your block', reply_markup=ReplyKeyboardMarkup(stage1_blocks, one_time_keyboard=True))
        return BLOCK
    elif user_choice == 'Stage 2':
        await update.message.reply_text('Choose your block', reply_markup=ReplyKeyboardMarkup(stage2_blocks, one_time_keyboard=True))
        return BLOCK
    elif user_choice == 'Stage 3':
        await update.message.reply_text('Choose your block', reply_markup=ReplyKeyboardMarkup(stage3_blocks, one_time_keyboard=True))
        return BLOCK
    elif user_choice == 'Stage 4':
        await update.message.reply_text('Choose your block', reply_markup=ReplyKeyboardMarkup(stage4_blocks, one_time_keyboard=True))
        return BLOCK
    elif user_choice == 'Go Back':
        return await handle_university(update, context)
    else:
        await update.message.reply_text('Please choose a valid stage', reply_markup=ReplyKeyboardMarkup([['Go Back']], one_time_keyboard=True))
        return STAGE

async def handle_block(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # Handle block choice
    user_choice = update.message.text
    language = context.user_data.get('language')

    if user_choice == 'Go Back' or user_choice == 'گەرانەوە':  # Handle the Go Back option properly
        return await handle_stage(update, context)
    
    # Send message after selecting a block
    if language == 'English':
        await update.message.reply_text(f"I want {user_choice}")
        await update.message.reply_text("Forward this message above to @zankys", reply_markup=ReplyKeyboardMarkup([['Go Back']], one_time_keyboard=True))
    else:
        await update.message.reply_text(f"من دەیەمەوە {user_choice}")
        await update.message.reply_text("ئەو نامەیەی سەرەوە بنێرە بۆ @zankys", reply_markup=ReplyKeyboardMarkup([['گەرانەوە']], one_time_keyboard=True))

    return BLOCK  # Allow going back to choose again

def main() -> None:
    # Replace 'YOUR_TELEGRAM_BOT_TOKEN' with your actual bot token
    application = ApplicationBuilder().token('6718822120:AAGPIFaSCDpkiZI9RsnfsLcLT-cBaKMvgg4').build()

    # Add conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            LANGUAGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_language)],
            CHOICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_choice)],
            FAQ: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_faq)],
            UNIVERSITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_university)],
            STAGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_stage)],
            BLOCK: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_block)],
        },
        fallbacks=[CommandHandler('start', start)],
    )

    application.add_handler(conv_handler)

    # Start the Bot
    application.run_polling()

if __name__ == '__main__':
    main()
