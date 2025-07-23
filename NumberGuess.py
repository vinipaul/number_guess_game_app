import streamlit as stream
import random
if 'generated_number' not in stream.session_state:
    stream.session_state.generated_number=random.randint(1,100)
if 'chance'not in stream.session_state:
    stream.session_state.chance=0
if 'guessed' not in stream.session_state:
    stream.session_state.guessed=False
stream.title("NUMBER GUESS GAME")
stream.write("Guess a number between 1 and 100")
guess=stream.number_input("Enter your guess",min_value=1,max_value=100,step=1)
if stream.button("Submit your Guess"):
    stream.session_state.chance=stream.session_state.chance+1   
    if guess==stream.session_state.generated_number:
        stream.success(f"congrats!you guessed it right.you won at {stream.session_state.chance} chance")
        stream.session_state.guessed=True
    elif guess<stream.session_state.generated_number:
        stream.warning("your guess is too low!try again...")
    else :
        stream.warning("your guess is too high!try again...")
if stream.session_state.guessed:
    if stream.button("Play again"):
        stream.session_state.generated_number=random.randint(1,100) 
        stream.session_state.guessed=False