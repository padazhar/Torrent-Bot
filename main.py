
import telebot
import pandas as pd
from telebot import types
from telegram.constants import ParseMode

import main as tor
from main import py1337x
import time
import asyncio

TOKEN = "5982978789:AAFM78GlOiEmV0tZqAFNNOj9YSOE5wSTK9Q"
bot = telebot.TeleBot(TOKEN)

quality_options = ['720p', '1080p']  # Available quality options

# Assuming you have a DataFrame named 'movies_df' containing movie data
movies_df = pd.DataFrame({'name': ['Movie 1', 'Movie 2', 'Movie 3']})
series_df = pd.DataFrame({'name': ['Series 1', 'Series 2', 'Series 3']})




@bot.message_handler(commands=['Movie'])
def send_option_message1(message):
    bot.send_message(chat_id=message.chat.id, text="Provide Name of the Movie")
    bot.register_next_step_handler(message, ask_quality_movie)


def ask_quality_movie(message):
    movie_name = message.text
    markup = types.ReplyKeyboardMarkup(row_width=2)
    quality_buttons = [types.KeyboardButton(quality) for quality in quality_options]
    markup.add(*quality_buttons)
    bot.send_message(chat_id=message.chat.id, text="Choose preferred quality:", reply_markup=markup)
    bot.register_next_step_handler(message, process_movie_choice, movie_name)


def process_movie_choice(message, movie_name):
    chosen_quality = message.text
    confirm_markup = types.ReplyKeyboardMarkup(row_width=2)
    confirm_buttons = [types.KeyboardButton("Yes"), types.KeyboardButton("No"), types.KeyboardButton("/Options")]
    confirm_markup.add(*confirm_buttons)
    bot.send_message(chat_id=message.chat.id, text=f"You selected '{movie_name}' in {chosen_quality} quality. Confirm?",
                     reply_markup=confirm_markup)
    bot.register_next_step_handler(message, process_movie_confirmation, movie_name, chosen_quality)
    if message.text == '/Options':
        send_welcome(message)


def process_movie_confirmation(message, movie_name, chosen_quality):
    if message.text.lower() == 'yes':
        # Process the movie choice and quality here
        obj = py1337x
        movies_df = tor.search_torrents(obj, movie_name, "1337x.to", chosen_quality,"movies")
        time.sleep(1)
        filtered_movies = movies_df.loc[movies_df['name'].str.contains(movie_name, case=False)]

        final_data = filtered_movies.copy()
        final_data['final'] = filtered_movies['name'] + " - " + filtered_movies['seeders'] + " - " + filtered_movies[
            'size']
        start = 1
        final_data.insert(0, 'ID', [str(idt) for idt in range(start, start + final_data.shape[0])])
        final_data['name'] = final_data['ID'] + ". " + final_data['final']
        if not filtered_movies.empty:
            movie_names = final_data['name'].values.tolist()
            movie_names1 = movie_names[0:4]
            movie_names2 = movie_names[5:9]
            bot.send_message(chat_id=message.chat.id,
                             text=f"Movies with the name '{movie_name}' in {chosen_quality} quality:\n\n" + "\n".join(
                                 movie_names1))
            try:
                bot.send_message(chat_id=message.chat.id,
                                 text=f"Movies with the name '{movie_name}' in {chosen_quality} quality:\n\n" + "\n".join(
                                     movie_names2))
            except:
                bot.send_message(chat_id=message.chat.id,text="Sorry No More Links")
            bot.register_next_step_handler(message, get_link, final_data)
        else:
            bot.send_message(chat_id=message.chat.id,
                             text=f"No movies found with the name '{movie_name}' in {chosen_quality} quality.")
    elif message.text.lower() == 'no':
        edit_markup = types.ReplyKeyboardMarkup(row_width=2)
        edit_buttons = [types.KeyboardButton("Edit Movie Name"), types.KeyboardButton("Edit Quality"),
                        types.KeyboardButton("Go Back")]
        edit_markup.add(*edit_buttons)
        bot.send_message(chat_id=message.chat.id, text="What would you like to edit?", reply_markup=edit_markup)
        bot.register_next_step_handler(message, process_movie_edit_choice, movie_name, chosen_quality)
    elif message.text.lower() == 'go back':
        send_welcome(message)


def process_movie_edit_choice(message, movie_name, chosen_quality):
    if message.text.lower() == 'edit movie name':
        bot.send_message(chat_id=message.chat.id, text="Please provide a new movie name:")
        bot.register_next_step_handler(message, ask_quality_movie)
    elif message.text.lower() == 'edit quality':
        bot.send_message(chat_id=message.chat.id, text="Choose a new preferred quality:")
        bot.register_next_step_handler(message, process_movie_choice, movie_name)
    elif message.text.lower() == 'go back':
        send_welcome(message)





@bot.message_handler(commands=['Series'])
def send_option_message2(message):
    bot.send_message(chat_id=message.chat.id, text="Provide Name of the Series")
    bot.register_next_step_handler(message, ask_quality_series)


def ask_quality_series(message):
    series_name = message.text
    markup = types.ReplyKeyboardMarkup(row_width=2)
    quality_buttons = [types.KeyboardButton(quality) for quality in quality_options]
    markup.add(*quality_buttons)
    bot.send_message(chat_id=message.chat.id, text="Choose preferred quality:", reply_markup=markup)
    bot.register_next_step_handler(message, process_series_choice, series_name)


def process_series_choice(message, series_name):
    chosen_quality = message.text
    confirm_markup = types.ReplyKeyboardMarkup(row_width=2)
    confirm_buttons = [types.KeyboardButton("Yes"), types.KeyboardButton("No"), types.KeyboardButton("/Options")]
    confirm_markup.add(*confirm_buttons)
    bot.send_message(chat_id=message.chat.id,
                     text=f"You selected '{series_name}' in {chosen_quality} quality. Confirm?",
                     reply_markup=confirm_markup)
    bot.register_next_step_handler(message, process_series_confirmation, series_name, chosen_quality)
    if message.text == '/Options':
        send_welcome(message)


def process_series_confirmation(message, series_name, chosen_quality):
    if message.text.lower() == 'yes':
        # Process the series choice and quality here
        # Assuming you have a DataFrame named 'series_df' containing series data
        obj = py1337x
        series_df = tor.search_torrents(obj, series_name, "1337x.to", chosen_quality,"tv")
        time.sleep(1)
        filtered_series = series_df.loc[series_df['name'].str.contains(series_name, case=False)]
        final_data = filtered_series.copy()
        final_data['final'] = filtered_series['name'] + " - " + filtered_series['seeders'] + " - " + filtered_series[
            'size']
        start = 1
        final_data.insert(0, 'ID', [str(idt) for idt in range(start, start + final_data.shape[0])])
        final_data['name'] = final_data['ID'] + ". " + final_data['final']

        if not filtered_series.empty:
            series_names = final_data['final'].values.tolist()
            series_names1 = series_names[0:4]
            series_names2 = series_names[5:9]
            bot.send_message(chat_id=message.chat.id,
                             text=f"Series with the name '{series_name}' in {chosen_quality} quality:\n\n" + "\n".join(
                                 series_names1))
            try:
                bot.send_message(chat_id=message.chat.id,
                                 text=f"Series with the name '{series_name}' in {chosen_quality} quality:\n\n" + "\n".join(
                                     series_names2))
            except:
                bot.send_message(chat_id=message.chat.id,text="Sorry No More Links")
            bot.register_next_step_handler(message, get_link, final_data)
        else:
            bot.send_message(chat_id=message.chat.id,
                             text=f"No series found with the name '{series_name}' in {chosen_quality} quality.")
    elif message.text.lower() == 'no':
        edit_markup = types.ReplyKeyboardMarkup(row_width=2)
        edit_buttons = [types.KeyboardButton("Edit Series Name"), types.KeyboardButton("Edit Quality"),
                        types.KeyboardButton("Go Back")]
        edit_markup.add(*edit_buttons)
        bot.send_message(chat_id=message.chat.id, text="What would you like to edit?", reply_markup=edit_markup)
        bot.register_next_step_handler(message, process_series_edit_choice, series_name, chosen_quality)
    elif message.text.lower() == 'go back':
        send_welcome(message)


def process_series_edit_choice(message, series_name, chosen_quality):
    if message.text.lower() == 'edit series name':
        bot.send_message(chat_id=message.chat.id, text="Please provide a new series name:")
        bot.register_next_step_handler(message, ask_quality_series)
    elif message.text.lower() == 'edit quality':
        bot.send_message(chat_id=message.chat.id, text="Choose a new preferred quality:")
        bot.register_next_step_handler(message, process_series_choice, series_name)
    elif message.text.lower() == 'go back':
        send_welcome(message)


def get_link(message, data):
    if message.text == '/Options':
        send_welcome(message)
    else:
        data = data[data['ID'] == message.text]
        print(data['torrentId'].values[0])
        obj = py1337x
        movies_link = tor.get_magnet(obj, data['torrentId'].values[0], "1337x.to")
        print(movies_link['magnetLink'].values[0])
        bot.send_message(chat_id=message.chat.id, text=movies_link['magnetLink'].values[0])


@bot.message_handler(commands=['Options'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    btn1 = types.KeyboardButton("/Movie")
    btn2 = types.KeyboardButton("/Series")
    btn3 = types.KeyboardButton("/Close")
    markup.add(btn1, btn2, btn3)
    bot.send_message(chat_id=message.chat.id, text="What do you want", reply_markup=markup)


@bot.message_handler(commands=['Close'])
def send_close_message(message):
    markup = types.ReplyKeyboardRemove(selective=False)
    bot.send_message(chat_id=message.chat.id, text="Bye", reply_markup=markup)


@bot.inline_handler(lambda query: query.query == 'text')
def query_text(inline_query):
    try:
        r = types.InlineQueryResultArticle('1', 'Result', types.InputTextMessageContent('Result message.'))
        r2 = types.InlineQueryResultArticle('2', 'Result2', types.InputTextMessageContent('Result message2.'))
        bot.answer_inline_query(inline_query.id, [r, r2])
    except Exception as e:
        print(e)


bot.polling()
