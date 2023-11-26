import emoji, random, os, json
from . import *

emojis = [
    '🍔', '🍕', '🍟', '🌮', '🌭', '🍣', '🍦', '🍧', '🍭', '🍫', '🍩', '🍪', '🍰', '🥧', '🍎',
    '💐', '🌸', '🌷', '🌹', '🌺', '🌻', '🌼', '🏵️', '🌱', '🌲', '🌳', '🌴', '🌵', '🌾', '🌿', '🍀',
    '🟥', '🟧', '🟨', '🟩', '🟦', '🟪', '🟥', '🟧', '🟨', '🟩', '🟦', '🟪', '🟥', '🟧', '🟨', '🟩',
    '🚕', '🚆', '🚢', '🚁', '🚀', '🚲', '🚑', '🚒', '🛴', '🛵', '🚜', '🏍️', '🛺', '🛸', '🚁',
    '🏠', '🏡', '🏢', '🏣', '🏥', '🏦', '🏨', '🏩', '⛪', '🏪', '🏫', '🏬', '🏭', '🏯', '🏰',
    '⌚', '📱', '💻', '⌨️', '🖱️', '🖨️', '🕹️', '📷', '🎥', '🎮', '🎧', '📺', '📻', '💽', '💾', '💿', '📀',
    '📚', '📖', '📔', '📒', '📕', '📗', '📘', '📙', '📓', '📃', '📜', '📄', '📰', '📑', '🔖', '📎',
    '☀️', '🌤️', '⛅', '🌦️', '🌧️', '⛈️', '🌩️', '🌨️', '❄️', '☃️', '🌬️', '💨', '🌪️', '🌫️', '🌊', '🌋',
    '🍇', '🍈', '🍉', '🍊', '🍋', '🍌', '🍍', '🍎', '🍏', '🍐', '🍒', '🍓', '🥭', '🍕', '🍖', '🍗', '🍘', '🍙',
    '🥞', '🍤', '🍥', '🍣', '🍱', '🍛', '🍜', '🍝', '🍠', '🍢', '🍤', '🍥', '🍦', '🍧', '🍨', '🍩', '🍪', '🍫', '🍬',
    '🍮', '🍯', '🍼', '🥛', '🍵', '🍶', '🍾', '🍷', '🍸', '🍹', '🍺', '🍻', '🥂', '🥃', '🥤', '🍽️', '🍴', '🥄',
    '🎭', '🎨', '🎤', '🎧', '🎼', '🎹', '🥁', '🎷', '🎺', '🎸', '🎻', '🎬', '🎮', '👾', '🎲'
]

def getRandomEmojis():
    return random.choice(emojis)
    em = emojis.replace(" ", "")
    return em[random.randint(0, len(em) - 1)]

def splitList(lis, index=4):
    newList = []
    while lis:
        sub = lis[:index]
        newList.append(sub)
        lis = lis[index:]
    return newList

@Client.on_command("createrole")
async def createRoles(ctx: BotContext[CommandEvent]):
    m = ctx.event.message
#    if m.receiver_id:
 #       return await m.send("Use this command in group!")
    try:
        param = m.message.split(maxsplit=1)[1]
    except IndexError:
        await m.send("Provide roles to create post!")
        return
    roles = []
    print(param)
    for msg in param.split("\n"):
        for msg in msg.split():
            if msg.strip():         
                roles.append(msg.strip())
    if not roles:
        await m.send("Please provide valid roles!")
        return
    message = ""
    roleBox = splitList(roles)
    usedEmojis = []
    print(roleBox)
    buttons = []
    for index, rolerow in enumerate(roleBox):
        bt = []
        for y, role in enumerate(rolerow):
            emoji = getRandomEmojis()
            usedEmojis.append(emoji)
            message += f"{emoji}: {role}\n"
            bt.append(InlineKeyboardButton(
              emoji,
                callback_data=f"mrkr_{index}_{y}"
            ))
        buttons.append(bt)
    await m.send(f"Pick your role:\n\n{message}", inline_markup=InlineMarkup(buttons))    

@Client.on_callback_query(filters.regexp(r"mrkr_(.*)"))
async def onCallback(ctx: BotContext[CallbackQueryEvent]):
    m = ctx.event.message
    index = [int(a) for a in ctx.event.callback_data.split("_")[1:]]
    buttons = m.inline_markup.inline_keyboard
    clicked = buttons[index[0]][index[1]]
    if " " not in clicked.text:
        em = clicked.text
        clicked.text += " 1"
    else:
        react = clicked.text.split(" ")
        em = react[0]
        clicked.text = react[0] + f" {int(react[1]) + 1}"
    getrole = m.message.split("\n\n", maxsplit=1)[-1].strip()
    findrole = list(filter(lambda x: x.split(":")[0] == em, getrole.split("\n")))
    cid = m.community_id
    if not findrole:
        return
    role = findrole[0].split(":")[-1].strip()
    roles = await app.get_roles(m.community_id)
 #   print(roles)
    member = await app.get_community_member(cid, ctx.event.action_by_id)
    roleId = None
    for erole in roles:
        if erole.name == role:
            roleId = erole.id
            break
    if not roleId:
        await app.add_role(cid, name=role, colour="000000")
        for erole in roles:
            if erole.name == role:
                roleId = erole.id
                break
    # print(pickOldroles, roleId, member)
    try:
        await app.add_member_to_role(cid, member.id, [roleId])
    except Exception as er:
        print(er)
        await ctx.event.answer("You already have that role!", show_alert=True)
        return
    await ctx.event.answer(f"Congrats! You have got a new role", show_alert=True)
    await m.edit_inline_markup(InlineMarkup(
        buttons
    ))