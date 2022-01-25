from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InputMediaPhoto,
    Message,
)

def play_markup(videoid, user_id):
    buttons= [
            [
                InlineKeyboardButton(text="▶️", callback_data=f'resumevc'),
                InlineKeyboardButton(text="⏸️", callback_data=f'pausevc'),
                InlineKeyboardButton(text="⏭️", callback_data=f'skipvc'),
                InlineKeyboardButton(text="⏹️", callback_data=f'stopvc')
            ],
            [
                InlineKeyboardButton(text="Owner", url="https://t.me/vckyclone"),
                InlineKeyboardButton(text="🗑 Close Menu", callback_data="close2"),
                InlineKeyboardButton(text="⚙ Menu", callback_data=f'other {videoid}|{user_id}'),
            ],
        ]
    return buttons 


def others_markup(videoid, user_id):
    buttons= [
            [
                InlineKeyboardButton(text="➕ Your Playlist", callback_data=f'playlist {videoid}|{user_id}'),
                InlineKeyboardButton(text="➕ Group Playlist", callback_data=f'group_playlist {videoid}|{user_id}')
            ],
            [
                InlineKeyboardButton(text="⬇️ Get Audio", callback_data=f"gets audio|{videoid}|{user_id}"),
                InlineKeyboardButton(text="⬇️ Get Video", callback_data=f"gets video|{videoid}|{user_id}")
            ],
            [
                InlineKeyboardButton(text="⬅️ Go Back", callback_data=f'goback {videoid}|{user_id}'),
                InlineKeyboardButton(text="🗑 Close Menu", callback_data=f'close2')
            ],
        ]
    return buttons 





play_keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("▶️", callback_data="resumevc"),
                    InlineKeyboardButton("⏸️", callback_data="pausevc"),
                    InlineKeyboardButton("⏭️", callback_data="skipvc"),
                    InlineKeyboardButton("⏹️", callback_data="stopvc")
                ],
                [
                    InlineKeyboardButton(
                        "Close Menu", callback_data="close"
                    )
                ]    
            ]
        )

def audio_markup(videoid, user_id):
    buttons= [
            [
                InlineKeyboardButton(text="▶️", callback_data=f'resumevc'),
                InlineKeyboardButton(text="⏸️", callback_data=f'pausevc'),
                InlineKeyboardButton(text="⏭️", callback_data=f'skipvc'),
                InlineKeyboardButton(text="⏹️", callback_data=f'stopvc')
            ],
            [
                InlineKeyboardButton(text="🗑 Close Menu", callback_data="close2")              
            ],
        ]
    return buttons 


def search_markup(ID1, ID2, ID3, ID4, ID5, duration1, duration2, duration3, duration4, duration5, user_id, query):
    buttons= [
            [
                InlineKeyboardButton(text="1️⃣", callback_data=f'Music2 {ID1}|{duration1}|{user_id}'),
                InlineKeyboardButton(text="2️⃣", callback_data=f'Music2 {ID2}|{duration2}|{user_id}'),
                InlineKeyboardButton(text="3️⃣", callback_data=f'Music2 {ID3}|{duration3}|{user_id}')
            ],
            [ 
                InlineKeyboardButton(text="4️⃣", callback_data=f'Music2 {ID4}|{duration4}|{user_id}'),
                InlineKeyboardButton(text="5️⃣", callback_data=f'Music2 {ID5}|{duration5}|{user_id}')
            ],
            [ 
                
                InlineKeyboardButton(text="⬅️", callback_data=f'popat 1|{query}|{user_id}'), 
                InlineKeyboardButton(text="🗑 Close", callback_data=f"ppcl2 smex|{user_id}") ,
                InlineKeyboardButton(text="➡️", callback_data=f'popat 1|{query}|{user_id}')             
            ],
        ]
    return buttons   

def search_markup2(ID6, ID7, ID8, ID9, ID10, duration6, duration7, duration8, duration9, duration10 ,user_id, query):
    buttons= [
            [
                InlineKeyboardButton(text="6️⃣", callback_data=f'Music2 {ID6}|{duration6}|{user_id}'),
                InlineKeyboardButton(text="7️⃣", callback_data=f'Music2 {ID7}|{duration7}|{user_id}'),
                InlineKeyboardButton(text="8️⃣", callback_data=f'Music2 {ID8}|{duration8}|{user_id}')
            ],
            [ 
                InlineKeyboardButton(text="9️⃣", callback_data=f'Music2 {ID9}|{duration9}|{user_id}'),
                InlineKeyboardButton(text="🔟", callback_data=f'Music2 {ID10}|{duration10}|{user_id}')
            ],
            [ 
                
                InlineKeyboardButton(text="⬅️", callback_data=f'popat 2|{query}|{user_id}'), 
                InlineKeyboardButton(text="🗑 Close", callback_data=f"ppcl2 smex|{user_id}") ,
                InlineKeyboardButton(text="⬅️", callback_data=f'popat 2|{query}|{user_id}')             
            ],
        ]
    return buttons 

def search_markupvideo(ID1, ID2, ID3, ID4, ID5, duration1, duration2, duration3, duration4, duration5, user_id, query):
    buttons= [
            [
                InlineKeyboardButton(text="1️⃣", callback_data=f'MusicVideo {ID1}|{duration1}|{user_id}'),
                InlineKeyboardButton(text="2️⃣", callback_data=f'MusicVideo {ID2}|{duration2}|{user_id}'),
                InlineKeyboardButton(text="3️⃣", callback_data=f'MusicVideo {ID3}|{duration3}|{user_id}')
            ],
            [ 
                InlineKeyboardButton(text="4️⃣", callback_data=f'MusicVideo {ID4}|{duration4}|{user_id}'),
                InlineKeyboardButton(text="5️⃣", callback_data=f'MusicVideo {ID5}|{duration5}|{user_id}')
            ],
            [ 
                
                InlineKeyboardButton(text="⬅️", callback_data=f'popat 1|{query}|{user_id}'), 
                InlineKeyboardButton(text="🗑 Close", callback_data=f"ppcl2 smex|{user_id}") ,
                InlineKeyboardButton(text="➡️", callback_data=f'popat 1|{query}|{user_id}')             
            ],
        ]
    return buttons   

def search_markupvideo2(ID6, ID7, ID8, ID9, ID10, duration6, duration7, duration8, duration9, duration10 ,user_id, query):
    buttons= [
            [
                InlineKeyboardButton(text="6️⃣", callback_data=f'MusicVideo {ID6}|{duration6}|{user_id}'),
                InlineKeyboardButton(text="7️⃣", callback_data=f'MusicVideo {ID7}|{duration7}|{user_id}'),
                InlineKeyboardButton(text="8️⃣", callback_data=f'MusicVideo {ID8}|{duration8}|{user_id}')
            ],
            [ 
                InlineKeyboardButton(text="9️⃣", callback_data=f'MusicVideo {ID9}|{duration9}|{user_id}'),
                InlineKeyboardButton(text="🔟", callback_data=f'MusicVideo {ID10}|{duration10}|{user_id}')
            ],
            [ 
                
                InlineKeyboardButton(text="⬅️", callback_data=f'popat 2|{query}|{user_id}'), 
                InlineKeyboardButton(text="🗑 Close", callback_data=f"ppcl2 smex|{user_id}") ,
                InlineKeyboardButton(text="⬅️", callback_data=f'popat 2|{query}|{user_id}')             
            ],
        ]
    return buttons 

def personal_markup(link):
    buttons= [
            [
                InlineKeyboardButton(text="Watch on Youtube", url=f'{link}')
            ],
            [ 
                InlineKeyboardButton(text="🗑 Close", callback_data=f'close')
            ],
        ]
    return buttons   
  
start_keyboard = InlineKeyboardMarkup( 
            [
                [
                    InlineKeyboardButton(
                        "📜 Commands", url="https://telegra.ph/Yui-music-11-04"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "🗑 Close Menu", callback_data="close2"
                    )
                ]    
            ]
        )
    
confirm_keyboard = InlineKeyboardMarkup( 
            [
                [
                    InlineKeyboardButton(
                        "Yes", callback_data="cbdel"
                    ),
                    InlineKeyboardButton(
                        "No", callback_data="close2"
                    )
                ]    
            ]
        )

confirm_group_keyboard = InlineKeyboardMarkup( 
            [
                [
                    InlineKeyboardButton(
                        "Yes", callback_data="cbgroupdel"
                    ),
                    InlineKeyboardButton(
                        "No", callback_data="close2"
                    )
                ]    
            ]
        )

close_keyboard = InlineKeyboardMarkup( 
            [
                [
                    InlineKeyboardButton(
                        "🗑 Close", callback_data="close"
                    )
                ]    
            ]
        )

play_list_keyboard = InlineKeyboardMarkup( 
            [
                [
                    InlineKeyboardButton(
                        "Personal Playlist", callback_data="P_list"
                    ),
                    InlineKeyboardButton(
                        "Group's Playlist", callback_data="G_list"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "🗑 Close", callback_data="close"
                    )
                ]
            ]
        )

def playlist_markup(user_name, user_id):
    buttons= [
            [
                InlineKeyboardButton(text=f"Group's Playlist", callback_data=f'play_playlist {user_id}|group'),
            ],
            [
                InlineKeyboardButton(text=f"{user_name[:8]}'s Playlist", callback_data=f'play_playlist {user_id}|personal'),
            ],
            [
                InlineKeyboardButton(text="🗑 Close", callback_data="close2")              
            ],
        ]
    return buttons
