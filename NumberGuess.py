import base64
import os
import streamlit as stream
import random
import pandas as pd
# import psycopg2
import datetime
# con=psycopg2.connect(dsn="postgresql://postgres:postgresvini@localhost:5432/number_guess_game_db")
# cur=con.cursor()
# cur.execute("create table if not exists player_details_tb pl")
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Define the scope for accessing Google Sheets and Drive
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

# Use the service account JSON key file
creds = ServiceAccountCredentials.from_json_keyfile_name("user-tracking.json", scope)

# Authorize the client
client = gspread.authorize(creds)

# Open the Google Sheet (replace with your actual sheet name)
sheet = client.open("User Log").sheet1
if 'generated_number' not in stream.session_state:
    stream.session_state.generated_number=random.randint(1,100)
if 'chance'not in stream.session_state:
    stream.session_state.chance=1
if 'guessed' not in stream.session_state:
    stream.session_state.guessed=False
if 'player_name' not in stream.session_state:
    stream.session_state.player_name=""
if 'players_inserted' not in stream.session_state:
    stream.session_state.players_inserted=False
chances=0
date=datetime.date.today().isoformat()
flag=0
stream.title("NUMBER GUESS GAME")
stream.image("logo.png",width=200,)
stream.session_state.player_name=stream.text_input("Enter Your Name: ")
player_name=stream.session_state.player_name
stream.button("Let's Go")
def autoplay_audio(file_path):
    with open(file_path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
        stream.markdown(
        f"<audio autoplay><source src='data:audio/mp3;base64,{b64}' type='audio/mp3'></audio>",
        unsafe_allow_html=True,
    )

if player_name and stream.button:
    if not stream.session_state.players_inserted:
    #     cur.execute("insert into players (name,date,chances) values(%s,%s,%s) returning id;",( stream.session_state.player_name,date,stream.session_state.chance,))
    #     cur.connection.commit()
        players=[{
        "Name":player_name,
        "played_on":date,
        "Chances":stream.session_state.chance
        
    }]     
        df=pd.DataFrame(players)
        df.to_csv("players.csv",mode="a",header=True,index=False)
        sheet.append_row([stream.session_state.player_name, date,stream.session_state.chance])
        stream.session_state.players_inserted=True
    stream.session_state.player_name=player_name
    if player_name.lower() in ("rejosh",):
        stream.write(f"Hi Rejoshetta")
    else:
        stream.write(f"Welcome {stream.session_state.player_name.capitalize()}")
    stream.write("I have  a number between 1 and 100.Can you guess it?")
    stream.write(f"chance {stream.session_state.chance}")
    guess=stream.number_input("Enter your guess",min_value=1,max_value=100,step=1)
    if stream.button("Submit your Guess"):
        chances=stream.session_state.chance
        stream.session_state.chance=stream.session_state.chance+1   
        if guess==stream.session_state.generated_number:
            stream.session_state.guessed=True
            autoplay_audio("cheering.mp3")
            stream.success(f"Congrats!you guessed it right.You won at  chance {stream.session_state.chance-1}!")
            player_details=[{
        "Name":player_name,
        "Number of Attempt":stream.session_state.chance-1,
        "Result":"win",
        
    }]     
            if stream.session_state.guessed==True: 
                result='win'
            else:
                result="failed"
            date=datetime.datetime.now()
            df=pd.DataFrame(player_details)
            df.to_csv("player_details.csv",mode="w",header=True,index=False)
            # cur.execute("insert into player_details (player_name,date,result,chances) values(%s,%s,%s,%s) returning player_id;",(player_name,date,result,stream.session_state.chance,))
            # cur.connection.commit()
        elif guess<stream.session_state.generated_number:
            stream.warning("your guess is too low!Try again...")
        else :
            stream.warning("your guess is too high!Try again...")
        
if stream.session_state.guessed==True:
    if stream.button("Game Summary") :
        df=pd.read_csv("player_details.csv")
        stream.dataframe(df)
    if stream.button("Play Again"):
            stream.warning("please press again")
            stream.session_state.chance=1
            stream.session_state.generated_number=random.randint(1,100) 
            stream.session_state.guessed=False
# if stream.session_state.players_inserted:  
#     cur.execute("update players set chances=%s where name=%s and date=%s",((stream.session_state.chance)-1,stream.session_state.player_name,date))
#     con.commit()