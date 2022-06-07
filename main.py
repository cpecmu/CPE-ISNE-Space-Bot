import os
import discord
import asyncio
import config
import bot_messages
import channel_ids
import role_ids
from discord.ext import commands, tasks
from replit import db
from keep_alive import keep_alive
##################

if config.flush_db:
  for key in db.keys():
    del db[key]
    
##################
    
intents = discord.Intents.default()
intents.members = True

bot = discord.Client(intents=intents)

##################

@bot.event
async def on_ready():
  print('Logged in as {0.user}\n'.format(bot))
  # print all roles
  guild = await get_guild()
  if config.debug_msg:
    print("\n".join([(str(r)+" = "+str(r.id)) for r in guild.roles]), '\n')
  
  # check for role message
  if not "role_msg_id" in db.keys():
    db["role_msg_id"] = await send_role_message()

  channel = bot.get_channel(channel_ids.roles)
  role_message = await channel.fetch_message(db["role_msg_id"])

  if config.debug_msg:
    print("Role Message:", role_message.content, '\n')

async def get_guild():
  return bot.get_guild(config.server_id) 

async def send_role_message():
  channel = bot.get_channel(channel_ids.roles)

  message = await channel.send(bot_messages.role_message)
  await message.add_reaction("🔵")
  await message.add_reaction("🟢")
  await message.add_reaction("🟣")
  
  return message.id

##################

@bot.event
async def on_member_join(member):
  if config.debug_msg:
    print("New user joined:",member.name, member.id)
  
  channel = bot.get_channel(channel_ids.welcome)
  await channel.send(bot_messages.welcome_message.format(member.id, channel_ids.rules))
  await asyncio.sleep(5)
  
  if not member.bot:
    await member.send(bot_messages.welcome_message_dm.format(member.id))
    await asyncio.sleep(5)

    await member.send(bot_messages.verify_question_1)

  key = "user_"+str(member.id)+"_verify_stage"
  db[key] = 0

@bot.event
async def on_message(message):
  if message.author == bot.user:
    return

  if message.content.startswith('$hi'):
    await message.channel.send('Hi to you!')
  
  # check DM
  if isinstance(message.channel, discord.DMChannel):
    if config.debug_msg:
      print("Direct Message:",message.author.name,":",message.content)
    # verification
    user = message.author
    key = "user_"+str(user.id)+"_verify_stage"
    if not key in db.keys():
      pass
    elif db[key] == 0:
      if "c++" in message.content.lower() or "c++" == message.content.lower():
        db[key] = 1

        await asyncio.sleep(3)
        await user.send(bot_messages.verify_question_2)
    elif db[key] == 1:
      if message.content.lower() == "1" or message.content.lower() == "2":
        db[key] = 2
        
        await asyncio.sleep(3)
        guild = await get_guild()
        member = await guild.fetch_member(user.id)
        role = discord.utils.get(guild.roles, id=role_ids.verified)
        await member.add_roles(role)
        await member.send(bot_messages.verified_message)
    
    
    
  

@bot.event
async def on_raw_reaction_add(payload):
  guild = await get_guild()
  channel = bot.get_channel(payload.channel_id)
  message = await channel.fetch_message(payload.message_id)
  
  user = await bot.fetch_user(payload.user_id)
  member = payload.member

  emoji = payload.emoji
  
  if user == bot.user:
    return
    
  # role message
  channel = bot.get_channel(channel_ids.roles)
  role_message = await channel.fetch_message(db["role_msg_id"])
  
  if message == role_message:
    guild = await get_guild()
    if str(emoji) == "🔵":
      role = discord.utils.get(guild.roles, id=role_ids.cpe)
      await member.add_roles(role)
    if str(emoji) == "🟢":
      role = discord.utils.get(guild.roles, id=role_ids.isne)
      await member.add_roles(role)


@bot.event
async def on_raw_reaction_remove(payload):
  guild = await get_guild()
  channel = bot.get_channel(payload.channel_id)
  message = await channel.fetch_message(payload.message_id)
  
  user = await bot.fetch_user(payload.user_id)
  member = await guild.fetch_member(payload.user_id)

  emoji = payload.emoji
  
  if user == bot.user:
    return
    
  # role message
  channel = bot.get_channel(channel_ids.roles)
  role_message = await channel.fetch_message(db["role_msg_id"])
  
  if message == role_message:
    guild = await get_guild()
    if str(emoji) == "🔵":
      role = discord.utils.get(guild.roles, id=role_ids.cpe)
      await member.remove_roles(role)
    if str(emoji) == "🟢":
      role = discord.utils.get(guild.roles, id=role_ids.isne)
      await member.remove_roles(role)


if config.keep_alive:
  keep_alive()
bot.run(os.environ['token'])

