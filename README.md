# Python Terminal Game

*** **THIS IS A WORK IN PROGRESS** ***

![Screenshot](/screenshot-connect-four.png "Python Terminal Connect Four")

## Description
This is a quick terminal game that will be written in Python. Being that the requirements are that it is played in the terminal itself, not launching a GUI, I wanted to start off with a game like Connect Four. Should this end up being too simplistic, I will likely use this repository for multiple games and create a second, more complex game.

## How many players will the game be for?
The game will initially be played by two players, but I may end up creating an AI to play it solo.

## What will the program do?
As many of us know, the basis of the game is to drop pieces into a grid and be the first one to get four in a row. This means the program will have to ask the players to choose which column they wish to place their next piece in, then switch back and forth between the players until one of them has connected four in a row.

## How will it work in a terminal?
This game should be fairly easy to implement in a terminal, as it will only require the screen to be cleared and rewritten to add the newly placed piece. The new piece to be added will be determined by the player choosing a column number to place the piece in.
