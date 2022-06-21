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

if config.display_db:
  for key in db.keys():
    print(key,db[key])

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
  # if not "role_msg_id" in db.keys():
  #   db["role_msg_id"] = await send_role_message()

  # channel = bot.get_channel(channel_ids.roles)
  # role_message = await channel.fetch_message(db["role_msg_id"])

  # if config.debug_msg:
  #   print("Role Message:", role_message.content, '\n')

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

    await member.send(bot_messages.verify_question_0)

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
    # question 0
    elif db[key] == 0:
      student_id = message.content
      year = int(student_id[:2])
      faculty = int(student_id[2:4])
      degree = int(student_id[4])
      curriculum = int(student_id[5])
      correct_curriculum = [0,1,2,5]

      print(student_id, year, faculty, degree, curriculum)

      await asyncio.sleep(3)
      if len(student_id) != 9 or year > config.current_year or faculty != 6 or degree != 1 or (curriculum not in correct_curriculum):
        await user.send(bot_messages.verify_invalid_0_0)
      else:
        if year < (config.current_year - 8):
          await user.send(bot_messages.verify_question_alumni_0)
          db[key] = "alumni"
        elif curriculum == 0 or curriculum == 2:
          await user.send(bot_messages.verify_question_cpe_0)
          db[key] = "cpe"
        elif curriculum == 1 or curriculum == 5:
          await user.send(bot_messages.verify_question_isne_0)
          db[key] = "isne"
    
    # question 0 (y/n)
    elif db[key] == "cpe" or db[key] == "isne" or db[key] == "alumni":
      await asyncio.sleep(3)
      await user.send(bot_messages.verify_question_1)
      if "y" in message.content.lower() or "y" == message.content.lower():
        db[key] = db[key]+"_y_1"
      elif "n" in message.content.lower() or "n" == message.content.lower():
        db[key] = db[key]+"_n_1"
        

    # question 1
    elif "1" in db[key]:
      await asyncio.sleep(3)
      if "c++" in message.content.lower() or "c++" == message.content.lower():
        db[key] = db[key][:-1]+"2"
        await user.send(bot_messages.verify_question_2)
      else:
        await user.send(bot_messages.verify_wrong_answer_tryagain)

    # question 2
    elif "2" in db[key]:
      await asyncio.sleep(3)
      if message.content.lower() == "4":
        db[key] = db[key][:-1]+"3"
        
        guild = await get_guild()
        member = await guild.fetch_member(user.id)
        
        role = discord.utils.get(guild.roles, id=role_ids.verified)
        await member.add_roles(role)

        if "cpe" in db[key]:
          roleid = role_ids.cpe
        elif "isne" in db[key]:
          roleid = role_ids.isne
        elif "alumni" in db[key]:
          roleid = role_ids.alumni
        role = discord.utils.get(guild.roles, id=roleid)
        await member.add_roles(role)
        
        await member.send(bot_messages.verified_message.format(role.name))
      else:
        await user.send(bot_messages.verify_wrong_answer_tryagain)

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

