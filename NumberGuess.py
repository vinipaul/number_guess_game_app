import base64
import streamlit as stream
import random
import pandas as pd
if 'generated_number' not in stream.session_state:
    stream.session_state.generated_number=random.randint(1,100)
if 'chance'not in stream.session_state:
    stream.session_state.chance=1
if 'guessed' not in stream.session_state:
    stream.session_state.guessed=False
if 'player_name' not in stream.session_state:
    stream.session_state.player_name=""
stream.title("NUMBER GUESS GAME")
stream.image("logo.png",width=200,)
player_name=stream.text_input("Enter Your Name: ")
stream.button("Let's Go")
def autoplay_audio(file_path):
    with open(file_path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
        stream.markdown(
        f"<audio autoplay><source src='data:audio/mp3;base64,{b64}' type='audio/mp3'></audio>",
        unsafe_allow_html=True,
    )
if player_name and stream.button:
    stream.session_state.player_name=player_name
    stream.write(f"Welcome {stream.session_state.player_name}")
    stream.write("I have  a number between 1 and 100.Can you guess it?")
    stream.write(f"chance {stream.session_state.chance}")
    guess=stream.number_input("Enter your guess",min_value=1,max_value=100,step=1)
    if stream.button("Submit your Guess"):
        stream.session_state.chance=stream.session_state.chance+1   
        if guess==stream.session_state.generated_number:
            autoplay_audio("cheering.mp3")
            stream.success(f"Congrats!you guessed it right.You won at  chance {stream.session_state.chance-1}!")
            player_details=[{
        "Name":player_name,
        "Number of Attempt":stream.session_state.chance,
        "Result":"win",
        
    }]
            df=pd.DataFrame(player_details)
            df.to_csv("player_details.csv",mode="w",header=True,index=False)
            stream.session_state.guessed=True
        elif guess<stream.session_state.generated_number:
            stream.warning("your guess is too low!Try again...")
        else :
            stream.warning("your guess is too high!Try again...")
if stream.session_state.guessed==True:
    if stream.button("summary of your game") :
        df=pd.read_csv("player_details.csv")
        stream.dataframe(df)
    if stream.button("Play Again"):
            stream.warning("please press again")
            stream.session_state.chance=1
            stream.session_state.generated_number=random.randint(1,100) 
            stream.session_state.guessed=False