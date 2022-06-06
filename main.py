import os
import discord
import config
import bot_messages
import channel_ids
import role_ids
from discord.ext import commands, tasks

from replit import db
#del db["role_msg_id"]

bot = commands.Bot(command_prefix = '.')

@bot.event
async def on_ready():
  print('Logged in as {0.user}'.format(bot))
  # print all roles
  guild = await get_guild() 
  print("\n".join([(str(r)+" = "+str(r.id)) for r in guild.roles]), '\n')
  
  # check for role message
  if not "role_msg_id" in db.keys():
    db["role_msg_id"] = await send_role_message()

  channel = bot.get_channel(channel_ids.bot_testing)
  role_message = await channel.fetch_message(db["role_msg_id"])

  print("Role Message:", role_message.content, '\n')

async def get_guild():
  return bot.get_guild(config.server_id) 

async def send_role_message():
  channel = discord.utils.get(bot.get_all_channels(), name='bot-testing')
  print(channel, channel.id, '\n')

  message = await channel.send(bot_messages.role_message)
  await message.add_reaction("🔵")
  await message.add_reaction("🟢")
  
  return message.id
  
@bot.event
async def on_message(message):
  if message.author == bot.user:
    return

  if message.content.startswith('$hi'):
    await message.channel.send('Hi to you!')

  channel = bot.get_channel(channel_ids.bot_testing)
  role_message = await channel.fetch_message(db["role_msg_id"])
  
  print(role_message.id, db["role_msg_id"])

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
  channel = bot.get_channel(channel_ids.bot_testing)
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
  channel = bot.get_channel(channel_ids.bot_testing)
  role_message = await channel.fetch_message(db["role_msg_id"])
  
  if message == role_message:
    guild = await get_guild()
    if str(emoji) == "🔵":
      role = discord.utils.get(guild.roles, id=role_ids.cpe)
      await member.remove_roles(role)
    if str(emoji) == "🟢":
      role = discord.utils.get(guild.roles, id=role_ids.isne)
      await member.remove_roles(role)



bot.run(os.environ['token'])

