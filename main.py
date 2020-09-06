import keepalive

#No touch above
import discord
from better_profanity import profanity
from discord.ext import commands
profanity.load_censor_words_from_file("profanity.txt")
client = commands.Bot(command_prefix="->")
traindex = []


'''
BELOW IS EVENTS
'''


@client.event
async def on_message(message):
  
  if profanity.contains_profanity(message.content):
    await message.channel.purge(limit=1)
    await message.channel.send("Don't swear")
    print("swear deleted")
    channel = message.guild.get_channel(739491604129251427)
    embed = discord.Embed(title="Message Deleted", color=0xb31212)
    embed.add_field(name="Swearing deleted:", value=message.content , inline=False)
    embed.add_field(name="Author:", value = message.author.name  ,inline=False)
    embed.add_field(name="ID:", value = message.author.id, inline = False)
    embed.add_field(name="Message ID:", value = message.id)
    if channel is None:
      print("Channel not found")
    else:
      await channel.send(embed=embed)
  
  elif message.channel.id == 615485719728750602 and message.content != "":
    print(message.attachments)
    if message.attachments != "":
      print("not pic")
      await message.channel.purge(limit=1)
    else:
      print("pic")  
  await client.process_commands(message)


@client.event
async def on_ready():

    print("Ready")



@client.event
async def on_raw_reaction_add(payload):
    if payload.channel_id==615478660790616093 and payload.emoji.name=="🛡️" :  
        print("Message correlation")
        guild_id=payload.guild_id
        guild = discord.utils.find(lambda g : g.id == guild_id, client.guilds)

        role = discord.utils.get(guild.roles, name = "Train novice")
        member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
        await member.add_roles(role)
        
        
@client.event        
async def on_message_delete(message):
  if profanity.contains_profanity(message.content):
    return
  else:
    print("deleted message")
    channel = message.guild.get_channel(739491604129251427)
    embed = discord.Embed(title="Message Deleted", color=0x690AA9)
    embed.add_field(name="Message deleted:", value=message.content , inline=False)
    embed.add_field(name="Author:", value = message.author.name  ,inline=False)
    embed.add_field(name="ID:", value = message.author.id, inline = False)
    embed.add_field(name="Message ID:", value = message.id)
    if channel is None:
        print("Channel not found")
    else:
        await channel.send(embed=embed)


@client.event
async def on_message_edit(beforemessage,aftermessage):
    channel = beforemessage.guild.get_channel(739491604129251427)
    embed = discord.Embed(title="Message Edited", color=0xf0c322)
    embed.add_field(name="Message before:", value=beforemessage.content , inline=False)
    embed.add_field(name="Message after:", value=aftermessage.content , inline=False)
    embed.add_field(name="Author:", value = beforemessage.author.name  ,inline=False)
    embed.add_field(name="ID:", value = beforemessage.author.id, inline = False)
    embed.add_field(name="Message ID:", value = aftermessage.id)
    if channel is None:
        print("Channel not found")
    else:
        await channel.send(embed=embed)    


@client.event 
async def on_raw_bulk_message_delete(payload):
  amount = len(payload.cached_messages) 
  embed = discord.Embed(title="Bulk delete", color=0x0c1a96)
  embed.add_field(name="Message IDs:", value =  payload.message_ids)
  embed.add_field(name = "Amount of messages:", value = amount , inline = True)
  guild = client.get_guild(payload.guild_id)
  channel = discord.utils.get(guild.channels, id = 739491604129251427)
  if channel is None:
    print("Error")
  else:
    await channel.send(embed=embed)    

'''
BELOW IS FOR COMMANDS
'''


@client.command()
@commands.has_role('Mod')
async def purge(ctx,amount=5):
    print ("purging" )
    await ctx.channel.purge(limit = amount + 1)

@client.command()
@commands.has_role('Co-Owner')
async def setplaying(ctx, message: str):
  await client.change_presence(activity=discord.Game(name=message))

@client.command()
@commands.has_role('Co-Owner')
async def setwatching(ctx, message: str):
  activity = discord.Activity(name= message, type=discord.ActivityType.watching)
  await client.change_presence(activity=activity)

@client.command()
@commands.has_role('Train novice')
async def traindex(ctx, train):
  with open('traindex.txt') as f:
    traindexs = f.read().splitlines()
    print(traindexs)
  for line in range(len(traindexs)):
    traincontents = traindexs[line].split(",")
    if traincontents[0] == train:
      await ctx.channel.send(traincontents)
      embed = discord.Embed(title="Traindex", color=0x0c1a96)
      
      embed.add_field(name="Name:", value =traincontents[0])
      embed.add_field(name = "Power:", value = traincontents[1] )
      embed.add_field(name = "Power type:", value = traincontents [2])
      embed.add_field(name= "Dimensions (M): ", value = traincontents[3])
      embed.set_image(url=traincontents[4])
      embed.set_author(name="Requested by:", url = "https://discordapp.com", icon_url = "https://cdn.discordapp.com/embed/avatars/0.png" )
      embed.set_footer(text = "Trains are sacred", icon_url = "https://media.discordapp.net/attachments/739458979381379072/752158619428061244/IMG_0063.JPG?width=624&height=468")
      await ctx.channel.send(embed=embed)  
  

    


      
      
      









# No touch below
    
keepalive.keep_alive()

    
client.run('NzM5MTg2ODY4OTg1NTI4MzQy.XyWzag.bs167pscooIcofOArGQA68rJNfI')



