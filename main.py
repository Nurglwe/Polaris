import keepalive
#No touch above
from better_profanity import profanity
from discord.ext import commands
import time,calendar,os,json,discord,requests
from fuzzywuzzy import fuzz
profanity.load_censor_words_from_file("profanity.txt")
client = commands.Bot(command_prefix="->")
traindex = []

#Commenting in progress
#Contact me on discord at Nurglwe#8387 if you want 


'''
BELOW IS EVENTS
'''


@client.event
async def on_member_join(payload):
  with open("join.txt","r") as f:
    data = json.load(f)
  with open("banned.txt",'r') as f:
    bans=json.load(f)
  guild = discord.utils.get(client.guilds, id=int(os.getenv("GUILD")))
  channel=discord.utils.get(guild.channels, id = int(os.getenv("DELC")))#del channel
  if str(payload.id) in bans:
    await payload.ban( reason = "Banned")
    print("Banned user")
  invs= await guild.invites()
  for x in invs:
    y=x.code
    if not(y in data):
      print("Not found")
      b={y:0}
      data.update(b)
    with open("join.txt","w") as f:
      json.dump(data,f)
  for x in invs:
    y=x.code
    if data[y]<x.uses:
      print(x.uses)
      v={y:x.uses}
      data.update(v)
      print("invite is "+y)
      break
  with open("join.txt",'w') as f:
    json.dump(data,f)
  
  embed = discord.Embed(title="Member join", color=0x0a27a6)#Puts message in deleted messages
  embed.add_field(name="Username:", value=payload , inline=False)
  embed.add_field(name="Join code:", value = y  ,inline=False)
  if channel is None:
    print("Channel not found")
  else:
    await channel.send(embed=embed)


     
  
  

@client.event
async def on_member_remove(member):
  print('Remove')
  guild = discord.utils.get(client.guilds, id = int(os.getenv("GUILD")) )#guild
  #Finds guild object
  channel = discord.utils.get(guild.channels, id = int(os.getenv("DELC")))#del channel
  #Finds channel object using guild object
  embed = discord.Embed(title='Member left', colour=0x780808)
  embed.add_field(name="Username:", value=member)
  embed.add_field(name="Member ID:", value=member.id)
  await channel.send(embed=embed)
# Uses channel to send name and ID of 

@client.event
async def on_message(message):

  #Swear filter
  if profanity.contains_profanity(message.content): #uses method provided by profanity to check message
    await message.channel.purge(limit=1) #Deletes message if it get picked up
    await message.channel.send("Don't swear") #could hook up to warn system?
    print("swear deleted")
    channel = message.guild.get_channel(int(os.getenv("DELC")))#del channel
    embed = discord.Embed(title="Message Deleted", color=0xb31212)#Puts message in deleted messages
    embed.add_field(name="Swearing deleted:", value=message.content , inline=False)
    embed.add_field(name="Author:", value = message.author.name  ,inline=False)
    embed.add_field(name="ID:", value = message.author.id, inline = False)
    embed.add_field(name="Message ID:", value = message.id)
    if channel is None:
      print("Channel not found")
    else:
      await channel.send(embed=embed)
  #Deletes messages if they're sent in picture only chat
  elif message.channel.id == int(os.getenv("PIC")) and message.content != "": #pictures
    try:#Uses error handling to check for link or image (If there's no attachment it will cause an error, which means it will delete the message)
      print(message.attachments[0])
      e = message.attachments[0]
      e = e.id #uses id function from discord?
      print(e)
    except:
      await message.channel.purge(limit=1)  
  await client.process_commands(message)


@client.event
async def on_ready():
  print("Ready")
  #Makes testing over and over easier




@client.event
async def on_raw_reaction_add(payload):
  #Verify reaction role
  if payload.channel_id==int(os.getenv("VER")) and   payload.emoji.name=="🛡️" :#verify  
      print("Message correlation")
      #uses different system as there's no ctx object like commands
      guild_id=payload.guild_id 
      guild = discord.utils.find(lambda g : g.id == guild_id, client.guilds)
      role = discord.utils.get(guild.roles, name = "Train novice")
      member = guild.get_member(payload.user_id)
      await member.add_roles(role)
        
        
@client.event        
async def on_message_delete(message):
  #Checks for swearing (message will already be deleted if it does)
  if profanity.contains_profanity(message.content):
    return
  else:
    print("deleted message")
  #Standard embed stuff
    channel = message.guild.get_channel(int(os.getenv("DELC")))#del channel
    link='https://discordapp.com/channels/{}/{}/{}'.format(message.guild.id,message.channel.id,message.id)
    embed = discord.Embed(title="Message Deleted", color=0x690AA9, description='Link to [message]({})'.format(link))
    if message.content != "":
      embed.add_field(name="Message deleted:", value=message.content , inline=False)
    embed.add_field(name="Author:", value = message.author.name  ,inline=False)
    embed.add_field(name="Author ID:", value = message.author.id, inline = False)
    embed.add_field(name="Message ID:", value = message.id)
    if channel is None:
        print("Channel not found")
    else:
        await channel.send(embed=embed)

@client.event
async def on_message_edit(beforemessage,aftermessage):
  #helps prevent filter bypass
  if beforemessage.content != aftermessage.content:
  #logs into channel
    channel = beforemessage.guild.get_channel(int(os.getenv("DELC")))#del channel
    link='https://discordapp.com/channels/{}/{}/{}'.format(beforemessage.guild.id,beforemessage.channel.id,beforemessage.id)
    embed = discord.Embed(title="Message Edited", color=0xf0c322,description='Link to [message]({})'.format(link))
    embed.add_field(name="Message before:", value=beforemessage.content , inline=False)
    embed.add_field(name="Message after:", value=aftermessage.content , inline=False)
    embed.add_field(name="Author:", value = beforemessage.author.name  ,inline=False)
    embed.add_field(name="ID:", value = beforemessage.author.id, inline = False)
    embed.add_field(name="Message ID:", value = aftermessage.id)
    if channel is None:
        print("Channel not found")
    else:
      await channel.send(embed=embed)   
  else:
    print('Link') 


@client.event 
async def on_raw_bulk_message_delete(payload):
  #Collects messages if needed for reports but doesn't log all the info (useful for spam and stuff)
  amount = len(payload.message_ids) 
  embed = discord.Embed(title="Bulk delete", color=0x0c1a96)
  embed.add_field(name="Message IDs:", value =  payload.message_ids)
  embed.add_field(name = "Amount of messages:", value = amount , inline = True)
  guild = client.get_guild(payload.guild_id)
  channel = discord.utils.get(guild.channels, id = int(os.getenv("DELC")))#del channel
  if channel is None:
    print("Error")
  else:
    await channel.send(embed=embed)    

  

'''
BELOW IS FOR COMMANDS
'''

@client.command()
async def invite (ctx):
  await ctx.channel.send('https://discord.com/api/oauth2/authorize?client_id=642403747850616864&permissions=0&scope=bot')

@client.command(brief="Call someone a spanner")
async def spanner(ctx,user:discord.User):
  #Sort of an insult, but sort of train related...
  e = 'https://media1.tenor.com/images/e01b325c047d38e4968b17a52aae0186/tenor.gif?itemid=5148623'
  e=str(e)
  await ctx.channel.send('<@{}> is an absolute spanner'.format(user.id))
  await ctx.channel.send(e)

@client.command(brief="Deletes messages (Mod+)")
@commands.has_role('Mod')
async def purge(ctx,amount=5):
  #bulk deletes, although stored in channel if needed
    print ("purging" )
    await ctx.channel.purge(limit = amount + 1)

@client.command(brief="Set the playing of the bot (Co-Owner)")
@commands.has_role('Co-Owner')
async def setplaying(ctx, message: str):
  #mainly for aesthetics, pretty neat
  await client.change_presence(activity=discord.Game(name=message))

@client.command(brief="Set the watching of the bot (Co-Owner)")
@commands.has_role('Co-Owner')
async def setwatching(ctx, message: str):
  #same as above
  activity = discord.Activity(name= message, type=discord.ActivityType.watching)
  await client.change_presence(activity=activity)


#intended to be main attraction
@client.command(brief="Call a train from the Traindex! (Any user)")
async def traindex(ctx, *args):
  train = ' '.join(args)
  with open('traindex.txt') as f:
    traindexs = f.read().splitlines()
  for line in range(len(traindexs)):
    traincontents = traindexs[line].split(",")
    train = train.lower()
 #above is the search algorithm
    if traincontents[0] == train:
      if traincontents[4] == '':
        traincontents[4] ='https://media.discordapp.net/attachments/615271081514893324/793798996846051378/Image_not_found.png'
      #finds picture, if none then it will replace it with a normal photo (helps bc I don't have to worry about finding a photo for now)
      found= True
      embed = discord.Embed(title="Traindex", color=0x0c1a96)
      embed.add_field(name="Name:", value =traincontents[0])
      embed.add_field(name = "Power:", value = traincontents[1] )
      embed.add_field(name = "Power type:", value = traincontents [2])
      embed.add_field(name= "Dimensions (M) Length-Width-Height: ", value = traincontents[3])
      embed.set_image(url=traincontents[4])
      embed.set_footer(text = "Trains are sacred", icon_url = "https://media.discordapp.net/attachments/739458979381379072/752158619428061244/IMG_0063.JPG?width=624&height=468")
      await ctx.channel.send(embed=embed)
      break
    else:
      #too lazy to comment the rest, figure it out future me 
      found= False
  if found == False:
    values = []
    trains = []
    for line in traindexs:
      contents = line.split(',')
      sim = fuzz.ratio(train, contents[0]) #fuzzy words to help finds similar trains
      if sim > 89:
        print(train)
        embed = discord.Embed(title="Traindex", color=0x0c1a96)
        embed.add_field(name="Name:", value =contents[0])
        embed.add_field(name = "Power:", value = contents[1] )
        embed.add_field(name = "Power type:", value = contents [2])
        embed.add_field(name= "Dimensions (Length-Width-Height): ", value = traincontents[3])
        embed.set_image(url=contents[4])
        embed.set_footer(text = "Fuzzywuzzy saved you", icon_url = "https://media.discordapp.net/attachments/739458979381379072/752158619428061244/IMG_0063.JPG?width=624&height=468")
        await ctx.channel.send(embed=embed)
        return
      values.append(sim)
      trains.append(contents[0])
    top3 = list(sorted(zip(values, trains), reverse=True))[:3]
    embed=discord.Embed(title='Error: Train not found', colour = 0x990000)
    embed.add_field(name='Oops',value = 'The number is the % match to your requested train and name of that train')
    embed.add_field(name='Sorry, the train was not found, possible trains you requested could be:',value = top3[0],inline= False)
    embed.add_field(name='Train 2', value =top3[1],inline=False)
    embed.add_field(name='Train 3',value = top3[2],inline= False)
    await ctx.channel.send(embed=embed)


@client.command(brief="Directly adds to traindex file (Mod+)")
@commands.has_role("Mod")
async def newtrain(ctx,train):
  #PRetty much puts the formatted input into the file
  file = open("traindex.txt","a")
  file.write("\n"+train)
  await ctx.channel.send("Added ", train)

@client.command(brief="Suggest a feature other than trains(Any user)")
async def suggest(ctx, *args):
  #suggest uses trello API to make a card into the to do part
  sugestee = ctx.author.name
  if ctx.channel.id == int(os.getenv("SUG")):#checks if in suggestions channel
    await ctx.channel.purge(limit = 1)
    helpme=" ".join(args) #very original variables, whaich join the args into a string so it can be parsed
    desc='Suggested by: '+sugestee +'\nSuggestion: '+helpme
    r=requests.post(url='https://api.trello.com/1/cards?key={}&token={}&name={}&idList=5f0c5f74e2601d4b6829ce51&desc={}'.format(str(os.getenv("KEY")),str(os.getenv("TRTOKEN")),helpme,desc)) #BTW env file is slocal to my account, which means that you need to make a file called .env to be able to store server codes/tokens
    embed = discord.Embed(title = "Suggestion", colour = 0x69ff91)
    embed.set_footer(text = "Suggestion complete")
    embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/739458979381379072/752567219677954139/IMG_0033.JPG")
    embed.add_field(name = "Person who suggested", value = sugestee )
    embed.add_field(name="Suggestion", value = helpme, inline = False )
    await ctx.channel.send(embed=embed) #makes and sends embed
    print(r)
  else:
    await ctx.channel.send("Error, wrong channel.")
    await ctx.channel.purge(limit = 2)  #tells people if in wrong channel


@client.command(brief="Gets invites(Mod+)")
@commands.has_role('Mod')
async def invites(ctx):
  #pulls a list of invites, was gonna use for anti-raid bot
  guild = discord.utils.get(client.guilds, id=int(os.getenv("GUILD")))#guild
  inviters= await guild.invites()
  uses = [x.uses for x in inviters]
  embed = discord.Embed(title="Invites")
  for i in inviters:
    embed.add_field(name="Invite:",value=i,inline=False)
  for u in uses:
    embed.add_field(name="Uses:",value=u,inline=False)
  await ctx.channel.send(embed=embed)

@client.command(brief="Bans a user(Mods+)")
@commands.has_role('Mod')
@commands.has_permissions(ban_members=True)
async def ban(ctx, user:discord.User, duration: int, *args):
  if duration == 0:
    await ctx.guild.ban(user)
  else:
    reason1 = " ".join(args)
    duration = duration *60*60*24 
    now = calendar.timegm(time.gmtime())
    now = int(now)
    when = now + duration
    with open('banned.txt') as f:
      data=json.load(f)
    user2 = user.id
    print(user.id)
    print(user2)
    y = {user2:when}
    data.update(y)
    with open('banned.txt','w') as f:
      json.dump(data,f)
    await ctx.guild.ban(user, delete_message_days=0,reason=reason1)
    await ctx.channel.send('{} banned'.format(user))

@client.command(brief='Checks all bans(Mod+)')
@commands.has_role('Mod')
async def checkbans(ctx):
  unbans = []
  with open('banned.txt') as f:
    data = json.load(f)
  for target in data:
    if data[target] <= calendar.timegm(time.gmtime()):
      guild = discord.utils.get(client.guilds, id = int(os.getenv("GUILD")))
      banlist = await guild.bans()
      for targete in banlist:
        if int(targete.user.id) == int(target): #I spent too long trying to convert this from usernames to user ids
          await ctx.guild.unban(targete.user)
          await ctx.channel.send('{} was unbanned'.format(targete.user.name)) 
          unbans.append(target)
  for un in unbans:
    print(un)
    del data[un]
  print(data)
  with open('banned.txt','w') as f:
    json.dump(data,f)
  print('complete')
          

@client.command(brief="Add new train suggestion (Any user)")
async def trainappend(ctx, *args):
  sugestee = ctx.author.name
  if ctx.channel.id == int(os.getenv("SUG")):
    time.sleep(1)#suggest
    await ctx.channel.purge(limit = 1)
    helpme=" ".join(args)
    desc='Suggested by: '+sugestee +'\nTrain suggestion: '+helpme
    r=requests.post(url='https://api.trello.com/1/cards?key={}&token={}&name={}&idList=5f0c5f74e2601d4b6829ce51&desc={}'.format(str(os.getenv("KEY")),str(os.getenv("TRTOKEN")),helpme,desc)) 
    embed = discord.Embed(title = "Train suggestion", colour = 0x11e4f7)
    embed.set_footer(text = "Suggestion complete")
    embed.set_thumbnail(url = "https://cdn.discordapp.com/attachments/739458979381379072/752567219677954139/IMG_0033.JPG")
    embed.add_field(name = "Person who suggested", value = sugestee )
    embed.add_field(name="Suggestion", value = helpme, inline = False )
    await ctx.channel.send(embed=embed)
    print(r)
  else:
    await ctx.channel.send("Error, wrong channel.")
    await ctx.channel.purge(limit = 2)  
  
@client.command()
async def ping(ctx):
    await ctx.send('Pong, {} Ms'.format(round(client.latency * 1000,2)))


@client.command(brief='Locks a channel (Mods+)')
@commands.has_role('Mod')
async def lock (ctx):
  roles = [
  747130286050902056,
  618887025747296277,
  618887927069671439,
  618887555038838808
  ]
  for put in roles:
    put2 = discord.utils.get(ctx.guild.roles, id=put)
    await ctx.channel.set_permissions(put2, send_messages=False, read_messages = True)

@client.command(brief='Unlocks a channel(Mods+)')
@commands.has_role('Mod')
async def unlock (ctx):
  roles = [
  747130286050902056,
  618887025747296277,
  618887927069671439,
  618887555038838808
  ]
  for put in roles:
    put2 = discord.utils.get(ctx.guild.roles, id=put)
    await ctx.channel.set_permissions(put2, send_messages=True, read_messages= True)

@client.command(brief='Bot joins channel and plays music (Any user)')
async def play(ctx, *args ):
  print(args)
  await ctx.channel.send("If only it were that easy :(")

# No touch below
    
keepalive.keep_alive()



token=os.getenv("TOKEN")    
client.run(token)

