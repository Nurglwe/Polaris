import keepalive
keepalive.keep_alive()
#No touch above
import discord
from better_profanity import profanity
from discord.ext import commands
profanity.load_censor_words_from_file("profanity.txt")
client = commands.Bot(command_prefix="->")



@client.event
async def on_message(message):
  if profanity.contains_profanity(message.content):
    await message.channel.purge(limit=1)
    await message.channel.send("Don't swear")
    await client.process_commands(message)

  elif message.channel.id==615485719728750602 and message.content != "":
    await message.channel.purge(limit=1)
    await client.process_commands(message)
  else:
    return
    await client.process_commands(message)
  await client.process_commands(message)
  
#@client.command()
@commands.has_role('Co-Owner')
async def unraid(ctx, invite ):
  print(ctx.guild.invites)
  for i in await ctx.guild.invites():
    if i.invitee == ctx.author:
      infor i in await ctx.guild.invites():
        if i.inviter == ctx.author:
          inviter = 1






@client.command()
@commands.has_role('Mod')
async def purge(ctx,amount=5):
    print ("purging")
    await ctx.channel.purge(limit = amount + 1)


        
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
        
        
        
        




async def on_message_delete(message):
    print("deleted message")
    channel = message.guild.get_channel
    embed = discord.Embed(title="Message Deleted", color=0x690AA9)
    embed.add_field(name="Message deleted:", value=message.content , inline=False)
    embed.add_field(name="Author:", value = message.author.name  ,inline=False)
    embed.add_field(name="ID:", value = message.author.id, inline = False)
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
    if channel is None:
        print("Channel not found")
    else:
        await channel.send(embed=embed)    

# No touch below
    

    
client.run('NzM5MTg2ODY4OTg1NTI4MzQy.XyWzag.bs167pscooIcofOArGQA68rJNfI')



