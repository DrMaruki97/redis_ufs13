# RedChat

Simple instant messaging software based on python and Redis database.

You can:
- Search your friends and add them
- Chat with your friends in real time
- Timed chat and group chat available
- Activate Do-Not-Disturb mode


## Table of Contents
1. [Installation](#installation)
2. [Usage](#usage)
3. [Configuration](#configuration)
5. [License](#license)
6. [Authors and Acknowledgments](#authors-and-acknowledgments)


## Installation

### Prerequisites
- Redis package of python
- How to install prerequisites
```cmd
pip install python 
pip install redis
```

### Installation Steps and Usage
- Clone the repo 
- Run the script 
```cmd
python RedChat.py
```
or
[try our GUI RedChat webapp](README_Interface.md)


## Usage and how it works

Guide:
1. Password must be 3-16 characters
2. Username must be unique
3. After sign up or login, the menu gets displayed, input the number of the function desired
4. You can't chat if you don't have any friends, use "2) Rubrica" command to add one first
5. So use 1) to chat, you can choose between "Timed" (the chat will be detroyed after 60 seconds from the last msg) or not
6. If you choose someone with prior chat history, you will get the last ten messages exchanged with time stamps
7. Close the chat with "esc"
8. You can activate the DnD mode (no one can send you messages) with command "3. Dnd"
9. You can change the password with command "4."
10. Use "5. Logout" to authenticate with a different account or exit the application

How it works:
- When you sign up the system:
  - If usr and pwd are valid, the user is added to the user list (a set)
  - There's a counter in Redis that increase with the number of users
  - An ID is created from that counter (f.e. the first user has id = "1")
  - A system bitmap is used to mark if a user is on DND mode (1 == active), each bit is a different user (we use the ID value to index it)
  - An istance with the username as key is saved, the value is the password hashed
  - Each user has a contact list, is made with a set in Redis
- When you chat:
  - An unique ID is created for each room (user1ID & user2ID, with user1 the user with the lower ID)
  - The chat history is saved in a z-set, the score is the time (unix epoch time)
  - The chat function itself is based on the use of a channel associated with the room ID
  - The partecipants of a chat are both publishers and subscribers, each message is published and saved in the z-set at the same time
  - Timed chat have a special character at the beggining of the room ID
  - If it is a timed chat, the system, with the use of Redis function EXPIRE, deletes the chat after 60 seconds from the last message
  - The group chat are intended as "public rooms" with custom alphabetical strings, you can enter is one of the public room or create one
- Other functions:
  - The password is hashed with a simple function
  - When the user changes his password, the system performs a SET and change the value of the password
  - When the user activate DnD mode, the system performs a SET and change the value of the bit with index = user_ID to "1"
  - You can only use the allowed numbers in the menu
  - When a friend is removed the user is removed from the contacts but the chat is still saved but not accessible

A note on the project:

The software had different stages, there were:
- Two terminal interfaces and one graphic interface that works (slightly) differently
- You can follow up the commits to discover the evolution of the project and the failed attempts
- Many files are saved in the "experimental" folder where you can check our experiments
- The definitive software (1.0) mains are RedChat (TUI and principal release) and Homepage (for the GUI)

## Configuration 

To use it with your own Redis database create and add to the config file your Redis server host name and password (work in progress)

## License

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

## Authors and Acknowledgments

@adish-rmr
@DrMaruki97
@alexandraazzena
@arct0r


