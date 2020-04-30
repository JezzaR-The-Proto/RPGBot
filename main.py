# RPGBot
# Discord bot that allows users to have an RPG-like experience.
# Created by JezzaR The Protogen#6483
import sqlite3, random, discord, logging, shutil, os, asyncio, requests, json
from discord.ext import commands, tasks
from discord.utils import get
from datetime import datetime
from itertools import cycle
from time import sleep
from PIL import Image, ImageFont, ImageDraw

# Init the DB
userDB = sqlite3.connect("users.db")
userCursor = userDB.cursor()

# Init Discord bot
prefix = "rpg "
client = commands.AutoShardedBot(command_prefix = commands.when_mentioned_or(prefix))
logger = logging.getLogger("discord")
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)
status = cycle(["Ready for action!",f"Create a character with {prefix} create!","Listening for commands"])
client.remove_command("help")
currentFolder = os.path.dirname(os.path.realpath(__file__))
# RPG Vars
xpRequired = [0,300,900,2700,]
helpPage = 1
helpInit = ""
helpMsg = ""
helpInitId = ""
maxPages = 9
enemyCurrentHP, enemyDef, enemyAtk, enemySpd, atk, defence, spd, currentHP, enemyLevel, enemyDamage, damage, fightMsg = 0,0,0,0,0,0,0,0,0,0,0,0
exploreOptions = json.load(open("exploreOptions.json"))

help1 = discord.Embed(title='RPGBot Help | Welcome', description="Welcome to RPGBot!\nI am currently still in development so bugs are expected.\n\nTo start, use `rpg create` to make a character!\nReact below to move through help pages.",color=0x00ff99)
help1.set_thumbnail(url="https://i.imgur.com/3eW4kff.png")
help1.set_footer(text=f"Page 1 of {maxPages}")
 
help2 = discord.Embed(title="RPGBot Help | Create Help", description="Classes:\nWarrior - Low Damage, High Defence, High Health, Low Speed\nArcher - Medium Damage, Medium Defence, Medium Health, Medium Speed\nRouge - Medium Damage, Low Defence, Low Health, High Speed\nDruid - Low Damage, Medium Defence, Medium Health, Medium Speed\nMage - High Damage, Low Defence, Low Health, High Speed",color=0x00ff99)
help2.set_thumbnail(url="https://i.imgur.com/3eW4kff.png")
help2.set_footer(text=f"Page 2 of {maxPages}")

help3 = discord.Embed(title="RPGBot Help | Warrior Help", description="The Warrior is a tank type class.\nThey have a low amount of damage and slow speed meaning that their enemies will usually attack faster and deal more dps.\nWithout their extra base health and defence, the warrior would be dead as soon as they enter any battle.",color=0x00ff99)
help3.set_thumbnail(url="https://i.imgur.com/3eW4kff.png")
help3.set_footer(text=f"Page 3 of {maxPages}")

help4 = discord.Embed(title="RPGBot Help | Archer Help",description="The Archer is a class with that has no specialty.\nThey have normal base stats that allows you to make a class that has whatever stats you want.\nThey attack from afar and so close ranged enemies can take a couple of turns to reach them.",color=0x00ff99)
help4.set_thumbnail(url="https://i.imgur.com/3eW4kff.png")
help4.set_footer(text=f"Page 4 of {maxPages}")

help5 = discord.Embed(title="RPGBot Help | Rouge Help",description="The Rouge is a class that specialises in hit-and-run attacks.\nThey have extremely low health and medium damage so they can't stand against an attack themselves but can disrupt enemies with their high speed.",color=0x00ff99)
help5.set_thumbnail(url="https://i.imgur.com/3eW4kff.png")
help5.set_footer(text=f"Page 5 of {maxPages}")

help6 = discord.Embed(title="RPGBot Help | Druid Help",description="The Druid is a support class.\nThey have lower damage output and normal health.\nThey are not known for being an attacking class and can heal teammates/themselves in a fight.",color=0x00ff99)
help6.set_thumbnail(url="https://i.imgur.com/3eW4kff.png")
help6.set_footer(text=f"Page 6 of {maxPages}")

help7 = discord.Embed(title="RPGBot Help | Mage Help",description="The Mage is a class that ***requires*** support.\nIf the mage does not have any support, they will die immediately upon joining any fight and without speed, they cannot get away with attacking enemies then running.\nWhile they are very fragile, they have massive damage output and can be a vital part in fighting bosses.",color=0x00ff99)
help7.set_thumbnail(url="https://i.imgur.com/3eW4kff.png")
help7.set_footer(text=f"Page 7 of {maxPages}")

help8 = discord.Embed(title="RPGBot Help | Guild Help",description="Guilds are groups that you can create to share money and items with other members.\nYou can make one with `rpg guild create` (Provided you have 10000 gold).",color=0x00ff99)
help8.set_thumbnail(url="https://i.imgur.com/3eW4kff.png")
help8.set_footer(text=f"Page 8 of {maxPages}")

help9 = discord.Embed(title="RPGBot Help | Guild Help Cont.",description="Guild Commands:\nguild create - Make a new guild.\nguild join (name) - Join the guild called (name).\nguild deposit (amount) - Deposit (amount) into the guild's bank.\nguild withdraw (amount) - Withdraw (amount) from the guild's bank.\nguild balance - View your guild's balance.",color=0x00ff99)
help9.set_thumbnail(url="https://i.imgur.com/3eW4kff.png")
help9.set_footer(text=f"Page 9 of {maxPages}")

createName = discord.Embed(title="Create a Character!",description="What name would you like for your character? (Less than 15 characters)\n***NOTE***\nWith the creation of a character, you agree to these rules:\n1) No abusing or benefiting from bugs or exploits\n2) Be friendly and kind to other players\n3) Trading in-game items or currency for real money or items directly comparable to currency is forbidden",color=0x00ff99)

createClass = discord.Embed(title="Create a Character!",description="What class would you like your character to be?\n(Warrior, Archer, Rouge, Druid, Mage)",color=0x00ff99)

def logs(author,reason): # Easier way to log
    with open("main.log", "a") as myfile:
        currentTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        myfile.write(f"[{currentTime}]: {author} sent {prefix}{reason}\n")

@client.event
async def on_ready(): # Log when bot starts up
    change_status.start()
    shutil.copy2(os.path.join(currentFolder,"users.db"),os.path.join(currentFolder,"users.db.bak"))
    with open("main.log", "a") as myfile:
        currentTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        myfile.write(f"[{currentTime}]: Bot ready\n")

@tasks.loop(seconds=15)
async def change_status(): # Changing status
    global prefix
    await client.change_presence(activity=discord.Game(next(status)))

@client.command()
async def help(ctx):
    global helpMsg, helpInit, helpPage, helpInitId
    helpPage = 1
    helpInit = ctx.author
    helpInitId = ctx.author.id
    helpMsg = await ctx.send("",embed=help1)
    await helpMsg.add_reaction("◀️")
    await helpMsg.add_reaction("⏹")
    await helpMsg.add_reaction("▶️")
    logs(ctx.author,"help")

@client.command()
async def create(ctx):
    def is_correct(m):
        return m.author == ctx.author

    userCursor.execute("SELECT name FROM users WHERE userID = ?",(ctx.author.id,))
    alreadyGotCharacter = userCursor.fetchall()
    if alreadyGotCharacter != []:
        await ctx.send("You already have a character. Multiple characters are not supported _yet_.")
        return

    await ctx.send("",embed=createName)
    try:
        playerName = await client.wait_for('message', check=is_correct, timeout=15.0)
        playerName = playerName.content
        if len(playerName) > 14:
            await ctx.send("That name is too long. Creation cancelled.")
    except asyncio.TimeoutError:
        await ctx.send("You took too long! Please retry!")
        playerName = ""
        playerClass = ""
        return
    
    await ctx.send("",embed=createClass)
    try:
        playerClass = await client.wait_for('message', check=is_correct, timeout=15.0)
        playerClass = playerClass.content
        playerClass = playerClass.lower()
    except asyncio.TimeoutError:
        await ctx.send("You took too long! Please retry!")
        playerName = ""
        playerClass = ""
        return
    
    if playerClass.lower() != "warrior" and playerClass.lower() != "archer" and playerClass.lower() != "rouge" and playerClass.lower() != "mage" and playerClass.lower() != "druid":
        await ctx.send("That is not a valid class. Please retry!")
        return
    
    if playerClass == "warrior":
        playerStr = 5
        playerDef = 20
        playerHP = 50
        playerSpd = 5
    elif playerClass == "archer":
        playerStr = 10
        playerDef = 10
        playerHP = 35
        playerSpd = 10
    elif playerClass == "rouge":
        playerStr = 10
        playerDef = 5
        playerHP = 20
        playerSpd = 15
    elif playerClass == "mage":
        playerStr = 15
        playerDef = 5
        playerHP = 20
        playerSpd = 15
    elif playerClass == "druid":
        playerStr = 5
        playerDef = 10
        playerHP = 30
        playerSpd = 10
    
    userCursor.execute("INSERT INTO users (userID, name, guild, class, signupDate, money, str, def, spd, currentHP, hp, level, xp) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)",(ctx.author.id, playerName, None, playerClass, datetime.now().strftime("%d-%m-%Y %H:%M:%S"), 100, playerStr, playerDef, playerSpd, playerHP, playerHP, 1, 0))
    userDB.commit()
    await ctx.send("Character created! Have fun!")

@client.command()
async def delete(ctx):
    userCursor.execute("SELECT name FROM users WHERE userID = ?",(ctx.author.id,))
    alreadyGotCharacter = userCursor.fetchall()
    if alreadyGotCharacter == []:
        await ctx.send("You do not have a character. Do `rpg create` to make one.")
        return
    
    await ctx.send("Are you ***sure*** you want to delete your character.\n***THIS CANNOT BE UNDONE***\n`y` or `n`")

    def is_correct(m):
        return m.author == ctx.author

    try:
        playerClass = await client.wait_for('message', check=is_correct, timeout=15.0)
        playerClass = playerClass.content
    except asyncio.TimeoutError:
        await ctx.send("You took too long! Deletion cancelled.")
    
    if playerClass != "y":
        await ctx.send("Deletion cancelled")
    else:
        userCursor.execute("DELETE FROM users WHERE userID = ?",(ctx.author.id,))
        userDB.commit()
        await ctx.send("Character deleted. 😢")

@client.command()
async def profile(ctx):
    img = requests.get(ctx.author.avatar_url_as(format="jpg",size=64))
    with open(os.path.join(currentFolder,"userAvatar.jpg"),"wb") as image:
        image.write(img.content)
    userAvatar = Image.open("userAvatar.jpg")
    background = Image.open("defaultBackground.png")
    background.paste(userAvatar,(0,0,64,64))
    draw = ImageDraw.Draw(background)
    font = ImageFont.truetype(os.path.join(currentFolder,"font.ttf"), 32)
    userCursor.execute("SELECT name FROM users WHERE userID = ?",(ctx.author.id,))
    tempText = userCursor.fetchall()
    if tempText == []:
        await ctx.send("You do not have a character.")
        return
    tempText = tempText[0][0]
    draw.text((74, 18),tempText,(0,0,0),font=font)

    userCursor.execute("SELECT level FROM users WHERE userID = ?",(ctx.author.id,))
    tempText = userCursor.fetchall()
    tempText = tempText[0][0]
    draw.text((290, 18),f"Level: {tempText}",(0,0,0),font=font)
    draw.text((26, 72),str(tempText),(255,255,255),font=font)
    draw.text((146, 72),str(tempText + 1),(255,255,255),font=font)

    userCursor.execute("SELECT level FROM users WHERE userID = ?",(ctx.author.id,))
    exp = userCursor.fetchall()
    exp = exp[0][0]
    levelProgressBar = 42 + round((exp/xpRequired[tempText])*100,0)
    draw.line((42,84,142,84), fill=(150,150,150), width=10)
    draw.line((42,84,int(levelProgressBar),84), fill=(255,255,255), width=10)

    userCursor.execute("SELECT class FROM users WHERE userID = ?",(ctx.author.id,))
    tempText = userCursor.fetchall()
    tempText = tempText[0][0]
    draw.text((200,72),f"Class: {tempText.capitalize()}",font=font)

    userCursor.execute("SELECT str FROM users WHERE userID = ?",(ctx.author.id,))
    tempText = userCursor.fetchall()
    tempText = tempText[0][0]
    draw.text((200,112),f"Attack: {tempText}",font=font)

    userCursor.execute("SELECT def FROM users WHERE userID = ?",(ctx.author.id,))
    tempText = userCursor.fetchall()
    tempText = tempText[0][0]
    draw.text((26,112),f"Defence: {tempText}",font=font)

    userCursor.execute("SELECT spd FROM users WHERE userID = ?",(ctx.author.id,))
    tempText = userCursor.fetchall()
    tempText = tempText[0][0]
    draw.text((200,152),f"Speed: {tempText}",font=font)

    userCursor.execute("SELECT hp FROM users WHERE userID = ?",(ctx.author.id,))
    tempText = userCursor.fetchall()
    tempText = tempText[0][0]
    draw.text((26,152),f"Health: {tempText}",font=font)

    userCursor.execute("SELECT money FROM users WHERE userID = ?",(ctx.author.id,))
    tempText = userCursor.fetchall()
    tempText = tempText[0][0]
    draw.text((26,192),f"Gold: {tempText}",font=font)

    userCursor.execute("SELECT guild FROM users WHERE userID = ?",(ctx.author.id,))
    tempText = userCursor.fetchall()
    tempText = tempText[0][0]
    userCursor.execute("SELECT name FROM guilds WHERE guildID = ?",(tempText,))
    tempText = userCursor.fetchall()
    tempText = tempText[0][0]
    draw.text((200,192),f'Guild: {tempText}',font=font)

    background.save(os.path.join(currentFolder,"userProfile.png"))
    await ctx.send("",file=discord.File("userProfile.png"))

@client.command()
async def guild(ctx, *guildArgs):
    try:
        args = guildArgs[0]
    except:
        await ctx.send("You need to enter something to do with the guild.")
        return
    try:
        args2 = guildArgs[1]
    except:
        noSecondArgs = True
        if noSecondArgs:
            noSecondArgs = False

    def is_correct(m):
        return m.author == ctx.author

    if args == "create":
        userCursor.execute("SELECT money FROM users WHERE userID = ?",(ctx.author.id,))
        userMoney = userCursor.fetchall()
        userMoney = userMoney[0][0]
        if userMoney < 10000:
            await ctx.send("You need at least 10000 gold to create a guild.")
            return
        await ctx.send("What would you like the name of your guild to be (Max 10 characters)?")
        try:
            guildName = await client.wait_for('message', check=is_correct, timeout=15.0)
            guildName = guildName.content
        except asyncio.TimeoutError:
            await ctx.send("You took too long! Guild creation cancelled.")
            return
        if len(guildName) > 10:
            await ctx.send("That name is too long. Please retry.")
            return
        if len(guildName.split(" ")) > 1:
            await ctx.send("A guild name cannot have any spaces in.")
            return
        userCursor.execute("SELECT name FROM guilds")
        guildNames = userCursor.fetchall()
        for name in guildNames:
            name = name[0]
            if guildName == name:
                await ctx.send("A guild with this name already exists. Please retry.")
                return
        userCursor.execute("SELECT guildID FROM guilds")
        guildIDs = userCursor.fetchall()
        if guildIDs == []:
            guildID = 1
        else:
            lastID = guildIDs[-1]
            lastID = lastID[0]
            guildID = lastID + 1
        userCursor.execute("INSERT INTO guilds(guildID, masterID, name, users, money, level, xp) VALUES(?,?,?,?,?,?,?)",(guildID, ctx.author.id,guildName,1,0,1,0))
        userDB.commit()
        userCursor.execute("UPDATE users SET guild = ? WHERE userID = ?",(guildID, ctx.author.id))
        userDB.commit()
        await ctx.send("Guild created!")
    elif args == "join":
        userCursor.execute("SELECT guild FROM users WHERE userID = ?",(ctx.author.id,))
        userGuild = userCursor.fetchall()
        userGuild = userGuild[0][0]
        if userGuild != None:
            await ctx.send("You are already in a guild.")
            return
        await ctx.send("What is the name of the guild you would like to join?")
        try:
            guildName = await client.wait_for('message', check=is_correct, timeout=15.0)
            guildName = guildName.content
        except asyncio.TimeoutError:
            await ctx.send("You took too long! Guild joining cancelled.")
            return
        userCursor.execute("SELECT guildID FROM guilds WHERE name = ?",(guildName,))
        userGuild = userCursor.fetchall()
        if userGuild == []:
            await ctx.send("There is no guild with this name (Guild names are case sensitive).")
            return
        userGuild = userGuild[0][0]
        userCursor.execute("UPDATE users SET guild = ? WHERE userID = ?",(userGuild, ctx.author.id))
        userDB.commit()
        userCursor.execute("SELECT users FROM guilds WHERE guildID = ?",(userGuild,))
        guildUsers = userCursor.fetchall()
        guildUsers = guildUsers[0][0]
        guildUsers += 1
        userCursor.execute("UPDATE guilds SET users = ? WHERE guildID = ?",(guildUsers, userGuild))
        userDB.commit()
        await ctx.send("Successfully joined guild!")
    elif args == "list":
        userCursor.execute("SELECT name FROM guilds ORDER BY users DESC")
        guilds = userCursor.fetchall()
        guilds = guilds[:10]
        await ctx.send(f"The top {len(guilds)} guilds (sorted by number of members) are:")
        for x in guilds:
            x = x[0]
            userCursor.execute("SELECT money FROM guilds WHERE name = ?",(x,))
            money = userCursor.fetchall()
            money = money[0][0]
            userCursor.execute("SELECT users FROM guilds WHERE name = ?",(x,))
            users = userCursor.fetchall()
            users = users[0][0]
            await ctx.send(f"Guild {x} has {users} members and {money} gold.")
    elif args == "deposit":
        userCursor.execute("SELECT money FROM users WHERE userID = ?",(ctx.author.id,))
        userMoney = userCursor.fetchall()[0][0]
        if int(args2) > int(userMoney):
            await ctx.send("You do not have enough gold.")
            return
        userCursor.execute("SELECT guild FROM users WHERE userID = ?",(ctx.author.id,))
        userGuild = userCursor.fetchall()[0][0]
        userCursor.execute("SELECT money FROM guilds WHERE guildID = ?",(userGuild,))
        guildMoney = userCursor.fetchall()[0][0]
        userCursor.execute("SELECT name FROM guilds WHERE guildID = ?",(userGuild,))
        guildName = userCursor.fetchall()[0][0]
        guildMoney += int(args2)
        userMoney -= int(args2)
        userCursor.execute("UPDATE users SET money = ? WHERE userID = ?",(userMoney, ctx.author.id))
        userCursor.execute("UPDATE guilds SET money = ? WHERE guildID = ?",(guildMoney, userGuild))
        userDB.commit()
        await ctx.send(f"Paid {str(args2)} gold into {guildName}'s bank.\n{guildName.capitalize()} now has {guildMoney} gold and you have {userMoney} gold.")
    elif args == "withdraw":
        userCursor.execute("SELECT money FROM users WHERE userID = ?",(ctx.author.id,))
        userMoney = userCursor.fetchall()[0][0]
        userCursor.execute("SELECT guild FROM users WHERE userID = ?",(ctx.author.id,))
        userGuild = userCursor.fetchall()[0][0]
        userCursor.execute("SELECT money FROM guilds WHERE guildID = ?",(userGuild,))
        guildMoney = userCursor.fetchall()[0][0]
        userCursor.execute("SELECT name FROM guilds WHERE guildID = ?",(userGuild,))
        guildName = userCursor.fetchall()[0][0]
        if int(args2) > int(guildMoney):
            await ctx.send(f"The guild does not have enough gold. It has {guildMoney} gold.")
            return
        guildMoney -= int(args2)
        userMoney += int(args2)
        userCursor.execute("UPDATE users SET money = ? WHERE userID = ?",(userMoney, ctx.author.id))
        userCursor.execute("UPDATE guilds SET money = ? WHERE guildID = ?",(guildMoney, userGuild))
        userDB.commit()
        await ctx.send(f"Withdrew {str(args2)} gold from {guildName}'s bank.\n{guildName.capitalize()} now has {guildMoney} gold and you have {userMoney} gold.")
    elif args == "balance":
        userCursor.execute("SELECT guild FROM users WHERE userID = ?",(ctx.author.id,))
        try:
            userGuild = userCursor.fetchall()[0][0]
        except:
            await ctx.send("You are not in a guild.")
            return
        userCursor.execute("SELECT money FROM guilds WHERE guildID = ?",(userGuild,))
        guildMoney = userCursor.fetchall()[0][0]
        userCursor.execute("SELECT name FROM guilds WHERE guildID = ?",(userGuild,))
        guildName = userCursor.fetchall()[0][0]
        await ctx.send(f"{guildName.capitalize()} has {guildMoney} gold in its bank.")
    elif args == "leave":
        userCursor.execute("SELECT guild FROM users WHERE userID = ?",(ctx.author.id,))
        try:
            userGuild = userCursor.fetchall()[0][0]
        except:
            await ctx.send("You are not in a guild.")
            return
        userCursor.execute("SELECT users FROM guilds WHERE guildID = ?",(userGuild,))
        guildUsers = userCursor.fetchall()[0][0]
        guildUsers -= 1
        userCursor.execute("UPDATE users SET guild = ? WHERE userID = ?",(None,ctx.author.id))
        userCursor.execute("UPDATE guilds SET users = ? WHERE guildID = ?",(guildUsers,userGuild))
        userDB.commit()
        userCursor.execute("SELECT name FROM guilds WHERE guildID = ?",(userGuild,))
        guildName = userCursor.fetchall()[0][0]
        await ctx.send(f"You have left {guildName.capitalize()}.")

@client.command()
async def explore(ctx):
    exploreVar = random.randint(0,99)
    whatHappened = exploreOptions["options"][exploreVar]["action"]
    if exploreVar >= 0 and exploreVar <= 49:
        await ctx.send(whatHappened)
    elif exploreVar >= 50 and exploreVar <= 89:
        await npcFight(ctx, whatHappened)
    else:
        userCursor.execute("SELECT inv FROM inventories WHERE userID = ?",(ctx.author.id,))
        currentInv = userCursor.fetchall()[0][0]
        if currentInv != None:
            currentInv = currentInv.split(",")
            itemIndex = currentInv.index(whatHappened)
            itemAmount = currentInv[itemIndex + 1]
            itemAmount += 1
            currentInv[itemIndex + 1] = str(itemAmount)
        else:
            currentInv = []
            currentInv.append(whatHappened)
            currentInv.append(str(1))
        finishedInv = ",".join(currentInv)
        userCursor.execute("UPDATE inventories SET inv = ? WHERE userID = ?",(finishedInv, ctx.author.id))
        userDB.commit()
        await ctx.send(f"You found a `{whatHappened}`")

async def npcFight(ctx, enemyName):
    global fightMsg, defence
    fightMsg = await ctx.send("Loading...")
    embed = fightDef(ctx.author.id, enemyName)
    await fightMsg.edit(content="",embed=embed)
    await fightMsg.add_reaction("⚔️")
    await fightMsg.add_reaction("🛡️")
    await fightMsg.add_reaction("🏃")
    def check(reaction, user):
        if user == ctx.author: 
            if str(reaction.emoji) == '⚔️':
                return True
            elif str(reaction.emoji) == "🛡️":
                return True
            elif str(reaction.emoji) == "🏃":
                return True
            else:
                return False
        else:
            return False
    fighting = True
    while fighting:
        try:
            reaction, user = await client.wait_for('reaction_add', timeout=30.0, check=check)
        except asyncio.TimeoutError:
            await ctx.send("You took too long without doing anything!")
            return
        if str(reaction.emoji) == "⚔️":
            await reaction.remove(user)
            if spd >= enemySpd:
                damageEnemy()
                damagePlayer(ctx.author.id)
                embed = redrawFightEmbed(ctx.author.id, enemyName)
                await fightMsg.edit(content="",embed=embed)
            else:
                damagePlayer(ctx.author.id)
                damageEnemy()
                embed = redrawFightEmbed(ctx.author.id, enemyName)
                await fightMsg.edit(content="",embed=embed)
        elif str(reaction.emoji) == "🛡️":
            defence += 5
            await reaction.remove(user)
            if spd >= enemySpd:
                damageEnemy()
                damagePlayer(ctx.author.id)
                embed = redrawFightEmbed(ctx.author.id, enemyName)
                await fightMsg.edit(content="",embed=embed)
            else:
                damagePlayer(ctx.author.id)
                damageEnemy()
                embed = redrawFightEmbed(ctx.author.id, enemyName)
                await fightMsg.edit(content="",embed=embed)
            defence -= 5
        elif str(reaction.emoji) == "🏃":
            if spd - 10 >= enemySpd:
                await fightMsg.edit(content="You successfully ran from `test enemy`!")
            elif spd < enemySpd:
                await fightMsg.edit(content="Your speed is too low, `test enemy` caught you running away!")
                sleep(1)
                damagePlayer(ctx.author.id)
                embed = redrawFightEmbed(ctx.author.id, enemyName)
                await fightMsg.edit(content="",embed=embed)
            elif spd == enemySpd:
                runAway = random.randint(0,1)
                if runAway == 1:
                    await fightMsg.edit(content="You successfully ran from `test enemy`!")
                else:
                    await fightMsg.edit(content="You have an equal speed to `test enemy` but they caught up to you!")
                    sleep(1)
                    damagePlayer(ctx.author.id)
                    embed = redrawFightEmbed(ctx.author.id, enemyName)
                    await fightMsg.edit(content="",embed=embed)
            else:
                spdDiff = (spd - enemySpd)*10
                runAway = random.randint(0,100)
                if runAway <= spdDiff:
                    await fightMsg.edit(content="You successfully ran from `test enemy`!")
                else:
                    await fightMsg.edit(content="You ran as fast as you could, but couldn't escape!")
                    sleep(1)
                    damagePlayer(ctx.author.id)
                    embed = redrawFightEmbed(ctx.author.id, enemyName)
                    await fightMsg.edit(content="",embed=embed)
        if currentHP <= 0:
            await fightMsg.edit(content="Oh no! You died!\nYou have lost half of your coins and all of your items.")
            userCursor.execute("SELECT money FROM users WHERE userID = ?",(ctx.author.id,))
            money = userCursor.fetchall()[0][0]
            money = money // 2
            userCursor.execute("UPDATE users SET money = ? WHERE userID = ?",(money, ctx.author.id))
            userDB.commit()
            userCursor.execute("SELECT hp FROM users WHERE userID = ?",(ctx.author.id,))
            hp = userCursor.fetchall()[0][0]
            userCursor.execute("UPDATE users SET currentHP = ? WHERE userID = ?",(hp,ctx.author.id))
            userDB.commit()
        elif enemyCurrentHP <= 0:
            fighting = False
    xp = random.randint(5,15)
    gold = random.randint(1,10)
    userCursor.execute("SELECT xp FROM users WHERE userID = ?",(ctx.author.id,))
    currentXP = userCursor.fetchall()[0][0]
    userCursor.execute("SELECT money FROM users WHERE userID = ?",(ctx.author.id,))
    currentMoney = userCursor.fetchall()[0][0]
    currentXP += xp
    userCursor.execute("SELECT level FROM users WHERE userID = ?",(ctx.author.id,))
    currentLevel = userCursor.fetchall()[0][0]
    if currentXP > xpRequired[currentLevel]:
        currentXP -= xpRequired[currentLevel]
        currentLevel += 1
        userCursor.execute("UPDATE users SET level = ? WHERE userID = ?",(currentLevel,ctx.author.id))
    currentMoney += gold
    userCursor.execute("UPDATE users SET xp = ? WHERE userID = ?",(currentXP,ctx.author.id))
    userDB.commit()
    userCursor.execute("UPDATE users SET money = ? WHERE userID = ?",(currentMoney,ctx.author.id))
    userDB.commit()
    await fightMsg.edit(content=f"Congrats! You beat `test enemy`! You earned {xp} xp and {gold} gold!")

def damageEnemy():
    global enemyCurrentHP, enemyDamage
    if atk - enemyDef <= 0:
        enemyDamage = 0
    else:
        enemyDamage = atk - enemyDef
    enemyCurrentHP -= enemyDamage

def damagePlayer(player):
    global currentHP, damage
    if enemyAtk - defence <= 0:
        damage = 0
    else:
        damage = enemyAtk - defence
    currentHP -= damage
    userCursor.execute("UPDATE users SET currentHP = ? WHERE userID = ?",(currentHP,player))
    userDB.commit()

def redrawFightEmbed(player, enemy):
    userCursor.execute("SELECT level FROM users WHERE userID = ?",(player,))
    level = userCursor.fetchall()[0][0]
    userCursor.execute("SELECT name FROM users WHERE userID = ?",(player,))
    name = userCursor.fetchall()[0][0]
    userCursor.execute("SELECT hp FROM users WHERE userID = ?",(player,))
    hp = userCursor.fetchall()[0][0]
    enemyHP = level * 50
    healthBar = round((currentHP/hp)*100,0)
    msg = ""
    x = 0
    while x <= healthBar:
        msg += "■"
        x += 10
    while x <= 100:
        msg += "□"
        x += 10
    enemyHealthBar = round((enemyCurrentHP/enemyHP)*100,0)
    enemyBar = ""
    x = 0
    while x <= enemyHealthBar:
        enemyBar += "■"
        x += 10
    while x <= 100:
        enemyBar += "□"
        x += 10
    msg = msg[:-1]
    enemyBar = enemyBar[1:]
    fightEmbed = discord.Embed(title=f"A wild `level {enemyLevel} {enemy}` approaches `{name}`!",description=f"{msg} - {currentHP}/{hp} vs {enemyCurrentHP}/{enemyHP} - {enemyBar}\nYou dealt {enemyDamage} damage to `{enemy}`\n`{enemy}` dealt {damage} damage to you.")
    return fightEmbed

def fightDef(player, enemy):
    global enemyCurrentHP, enemyDef, enemyAtk, enemySpd, atk, defence, spd, currentHP, enemyLevel
    userCursor.execute("SELECT level FROM users WHERE userID = ?",(player,))
    level = userCursor.fetchall()[0][0]
    enemyLevel = level + random.randint(0,3)
    enemyHP = level * 50
    enemyCurrentHP = enemyHP
    enemyDef = level * 5
    enemyAtk = level * 13
    enemySpd = level * 7
    userCursor.execute("SELECT str FROM users WHERE userID = ?",(player,))
    atk = userCursor.fetchall()[0][0]
    userCursor.execute("SELECT def FROM users WHERE userID = ?",(player,))
    defence = userCursor.fetchall()[0][0]
    userCursor.execute("SELECT spd FROM users WHERE userID = ?",(player,))
    spd = userCursor.fetchall()[0][0]
    userCursor.execute("SELECT hp FROM users WHERE userID = ?",(player,))
    hp = userCursor.fetchall()[0][0]
    userCursor.execute("SELECT name FROM users WHERE userID = ?",(player,))
    name = userCursor.fetchall()[0][0]
    currentHP = hp
    healthBar = round((currentHP/hp)*100,0)
    msg = ""
    x = 0
    while x <= healthBar:
        msg += "■"
        x += 10
    while x <= 100:
        msg += "□"
        x += 10
    enemyHealthBar = round((currentHP/hp)*100,0)
    enemyBar = ""
    x = 0
    if enemyHealthBar <= 0:
        enemyBar = "□□□□□□□□□□"
        x = 101
    while x <= enemyHealthBar:
        enemyBar += "■"
        x += 10
    while x <= 100:
        enemyBar += "□"
        x += 10
    fightEmbed = discord.Embed(title=f"A wild `level {enemyLevel} {enemy}` approaches `{name}`!",description=f"{msg} - {currentHP}/{hp} vs {enemyCurrentHP}/{enemyHP} - {enemyBar}\nReact below with what you want to do!")
    return fightEmbed

@client.event
async def on_reaction_add(reaction, user):
    global helpPage, helpMsg
    if reaction.emoji == "▶️":
        if reaction.message == helpMsg:
            if user == helpInit:
                await reaction.remove(user)
                if helpPage == 9:
                    helpChanged = False
                    return
                else:
                    helpPage += 1
                    helpChanged = True
    elif reaction.emoji == "◀️":
        if reaction.message == helpMsg:
            if user == helpInit:
                await reaction.remove(user)
                if helpPage == 1:
                    helpChanged = False
                    return
                else:
                    helpPage -= 1
                    helpChanged = True
    elif reaction.emoji == "⏹":
        if reaction.message == helpMsg:
            if user == helpInit:
                await helpMsg.delete()
                helpChanged = False
                return
    if helpChanged:
        if helpPage == 1:
            await helpMsg.edit(content="",embed=help1)
        elif helpPage == 2:
            await helpMsg.edit(content="",embed=help2)
        elif helpPage == 3:
            await helpMsg.edit(content="",embed=help3)
        elif helpPage == 4:
            await helpMsg.edit(content="",embed=help4)
        elif helpPage == 5:
            await helpMsg.edit(content="",embed=help5)
        elif helpPage == 6:
            await helpMsg.edit(content="",embed=help6)
        elif helpPage == 7:
            await helpMsg.edit(content="",embed=help7)
        elif helpPage == 8:
            await helpMsg.edit(content="",embed=help8)
        elif helpPage == 9:
            await helpMsg.edit(content="",embed=help9)
        helpChanged = False

# Start Discord Bot
client.run("Epic Bot Token Goes Here")
