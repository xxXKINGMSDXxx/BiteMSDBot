import discord
from discord.ext import commands
import langid,json
import re,string,asyncio
import emoji,time,os,io
from kep import keep_alive
from datetime import datetime, timedelta
import requests,random
#add emojis also t,ioo the letters
from discord import File

# Function to detect language and return result
from bs4 import BeautifulSoup

keep_alive()
#setting variables

def keyFinder(inputt):
  def is_valid_email(email):
      email_regex = r"^[^\s@]+@[^\s@]+\.[^\s@]+$"
      return bool(re.match(email_regex, email))
  url = None
  if is_valid_email(inputt) == False:
      url = f"https://biteyt.xyz/api?searchKeyByUID={inputt}"

  else:
      url = f"https://biteyt.xyz/api?searchKeyByEmail={inputt}"

  headers = {
      "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 11; SM-A205F Build/RP1A.200720.012)",
  }
  response = requests.request("GET", url, headers=headers)

  json_data = response.text
  if 'error'not in json_data:
      decoded_data = json.loads(json_data)

      keys = decoded_data["keys"]
      listat =[]
      for key in keys:
          listat.append(key['key'])
      if len(listat) == 0:
          return 'No Keys were Found'
      else:
          return f"Keys found: {listat}"
  else:
       return 'An Invalid UID Format Was Provided'


def write_config(data):
  with open('config.json', 'w') as file:
      json.dump(data, file, indent=4)

 #default value
def read_config():
  with open('config.json', 'r') as file:
    data = json.load(file)
    return data

config_data = read_config()

auto_handle = config_data['auto_handle']
bot_prefix = config_data['prefix']
def generator():
    url = "https://biteyt.xyz/getVip/GenerateLink.php"

    payload = "hidden_field=true"
    headers = {
        "authority": "biteyt.xyz",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "en-GB,en;q=0.9,ar-IQ;q=0.8,ar;q=0.7,en-US;q=0.6",
        "cache-control": "max-age=0",
        "content-type": "application/x-www-form-urlencoded",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    }

    r = requests.request("POST", url, data=payload, headers=headers).text
    print(r)

    soup=BeautifulSoup(r,'lxml')
    l = soup.find('input')
    l = l.get('value')
    return l
def detect_language(message,letters):
    message = message.content

    for emoji_key in emoji.EMOJI_DATA.keys():

        # Remove all emojis characters from message
        if emoji_key in message:
             message=message.replace(emoji_key,'')


    # Check if the message length is above the minimum threshold
    c0ll =[]
    for i in message:

        #if emoji.is_emoji(i) == True:
 #            continue


        if i in letters:

          c0ll.append(i)
        if i.isascii() == True and i.isalpha() == False:

          c0ll.append(i)
        if i.isascii() == False and i.isalpha() == False:

          c0ll.append(i)
    if len(''.join(c0ll)) < len(message):
                return 'please use ENGLISH only'
    else:
          return None

intents = discord.Intents.all()
intents.messages = True  # Enable the message content intent

# Create a bot instance with a command prefix and intents
bot = commands.Bot(command_prefix=bot_prefix, intents=intents)

# Minimum length for language detection

warns = {}
# Event: Triggered when the bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

# Event: Triggered when a message is received

whitelist=[769202208981385246,680713753242632222,140719012559454208,446786062325514270,557628352828014614]

@bot.event
async def on_message(message):
    file = open('chars.txt', 'r', encoding='utf-8')
    letters = file.read()
    file.close()
    letters = str(letters)
    config_data = read_config()
    auto_handle = config_data['auto_handle']
    # Ignore messages from the bot itself

    if message.author == bot.user:
      return


    ignoredchannel = 1101169389958602802



    # Store relevant information before deleting the message
    author_ = message.author.name
    #guild = message.author.guild.id
    author_id = message.author.id
    channel_id = message.channel.id
    channel = bot.get_channel(channel_id)
    channel_name = message.channel.name
    if message.author.bot and 'ticket' not in channel_name:
      return
    if detect_language(message,letters) == 'please use ENGLISH only' and message.author.id not in whitelist and 'ticket' not in channel_name and ignoredchannel != channel_id and not message.author.guild_permissions.administrator:

    # Delete the message
        await message.delete()
        # Send a reply using stored information

        botmsgg = await channel.send(f"Please use English Only <@{author_id}>")
        await asyncio.sleep(3)
        print(message.content)
        await botmsgg.delete()
        if author_ in warns:

            if warns[author_] == 3:
                #in on_message function timeout user for 5 min 

                duration = timedelta(minutes=5)
                await message.author.timeout(duration)
                print('Timeouted '+ author_)
            else:
                 warns[author_] += 1
        else:
             warns[author_] = 1
    # Process commands after handling language detection

    #now check auto handling
    if auto_handle:
        msg = message.content
        handling_str = 'YOU CAN CHOOSE ANY PRICE AND TELL OR USE THE FREE KEY WITH ONE DAY ADS'

        if handling_str.upper() in msg.upper():

            #creating embed for handle message
                new_channel_name = f't-{message.channel.name}'  # Add 't-' prefix
                try:
                  await message.channel.edit(name=new_channel_name)
                  print(f'Changed channel name to: {new_channel_name}')
                except discord.Forbidden:
                  print(f"Bot doesn't have permission to change channel name in {message.channel.name}")
                thumbnail_url = "https://cdn.discordapp.com/avatars/140719012559454208/2ae7101006255b2bd5e681b76ea8df47.png?size=4096"
                embed = discord.Embed(
                    title="AUTO-HANDLE",
                    description="**Hello This is Auto-Handle \n Seems you want vip key ? Here are commands that may help you !**",
                    color=discord.Color.red()
                )
                embed.set_thumbnail(url=thumbnail_url)
                embed.add_field(name="**`>prices`**", value="**Shows Vip Key Prices**", inline=True)
                embed.add_field(name="**`>methods`**", value="**Shows Available Methods For Paying**", inline=True)

                embed.set_footer(text="Thank you for choosing our VIP Mods !", icon_url=thumbnail_url)

                await channel.send(embed=embed)


    await bot.process_commands(message)
@bot.command(hidden = True)
async def bot_handling(ctx,stats):
    global auto_handle
    if stats == None:
        config_data['auto_handle'] = False
        write_config(config_data)#off
        await ctx.reply('⭕ Defualting to OFF ⭕')
    elif stats.lower() == 'on':
        config_data['auto_handle'] = True
        write_config(config_data)#on
        await ctx.reply('🔴 Bot Handling is ON 🔵')
    elif stats.lower() == 'off':
        config_data['auto_handle'] = False
        write_config(config_data)#off
        await ctx.reply('⭕ Bot Handling is OFF ⭕')
    else:
        await ctx.reply("Invalid Statement! Please Use `ON` or `OFF` ")


@bot.command()
async def methods(ctx):
    thumbnail_url = "https://cdn.discordapp.com/avatars/140719012559454208/2ae7101006255b2bd5e681b76ea8df47.png?size=4096"

    embed = discord.Embed(
        title="Methods",
        description="**This all available methods for paying you should ping or send proof after paying with the provided methods:**",
        color=discord.Color.red()
    )
    embed.set_thumbnail(url=thumbnail_url)
    embed.add_field(name="**`Paypal`**", value="**Pay to [Click here](https://www.paypal.me/BiteXjs?country.x=IN&locale.x=en_GB)**", inline=True)
    embed.add_field(name="**`Crypto`**", value="**Talk with us for more info about this method**", inline=True)
    embed.set_footer(text="Thank you for choosing our VIP Mods !", icon_url=thumbnail_url)
    await ctx.reply(embed=embed)

@bot.command()
async def joke(ctx): 
    try:
        # Fetch a random joke from an A PI
        response = requests.get("https://official-joke-api.appspot.com/jokes/random")
        data = response.json()
        if 'setup' in data and 'punchline' in data:
            setup = data['setup']
            punchline = data['punchline']
            await ctx.reply(f"**Joke**: {setup}\n**Punchline**: {punchline}")
        else:
            await ctx.send("Oops! I couldn't fetch a joke right now. Try again later.")
    except Exception as e:
        print(e)
        await ctx.send("Oops! I encountered an error while fetching a joke. Try again later.")


@bot.command(hidden=True)
async def meme(ctx):
    try:
        # Send a request to the Meme API
        response = requests.get("https://meme-api.com/gimme")
        print(response)
        if response.status_code == 200:
            data = response.json()
            meme_url = data["url"]
            title = data['title']

            # Create an embed with the meme information
            embed = discord.Embed(title=title, color=0x00ff00)
            embed.set_image(url=meme_url)

            # Send the embed with the meme picture
            await ctx.reply(embed=embed)
        else:
            await ctx.reply("Failed to fetch a meme.")
    except Exception as e:
        print(e)



@bot.command(aliases=["Findkey", "findkey", "biteslip","findKey"])
async def FindKey(ctx,data: str):
    if ctx.author.guild_permissions.administrator or ctx.author.id == 769202208981385246:
      result = keyFinder(data)
      await ctx.reply(f'**{result}**')
    else:
      await ctx.reply("**You don't have permission to use this command**")

@bot.command()
async def verfication(ctx):
  await ctx.reply('> open https://www.biteyt.xyz/site/ \n> solve captcha\n> go back again login')
  
@bot.command()
async def pat(ctx,user: str = None):
    def extract_user_id(input_str):
        match = re.match(r'<@!?(\d+)>', input_str)
        if match:
            return int(match.group(1))
        elif input_str.isnumeric():
            return int(input_str)
        return None

    if user is None:
        user = ctx.author
    else:
        user_id = extract_user_id(user)
        if user_id:
            user = bot.get_user(user_id)
        else:
            await ctx.reply("Invalid user mention or ID provided.")
            return
    r = requests.get("https://nekos.life/api/v2/img/pat")
    res = r.json()
    try:
        async with requests.Session() as session:
            async with session.get(res['url']) as resp:
                image = await resp.read()
        with io.BytesIO(image) as file:
            await ctx.send(user.mention, file=discord.File(file, f"exeter_kiss.gif"))
    except:
        em = discord.Embed(description='**Patting **'+user.mention)
        em.set_image(url=res['url'])
        await ctx.reply(embed=em)



@bot.command()
async def tutorial(ctx):
  await ctx.reply('https://youtu.be/XPsdY21G-cs?si=kYZxAuRAG6PZJNyN')
@bot.command()
async def prices(ctx):
    thumbnail_url = "https://cdn.discordapp.com/avatars/140719012559454208/2ae7101006255b2bd5e681b76ea8df47.png?size=4096"
    embed = discord.Embed(
        title="VIP Key Prices",
        description="Here are the prices for VIP keys:",
        color=discord.Color.red()
    )
    embed.set_thumbnail(url=thumbnail_url)
    embed.add_field(name="**$5 USD**", value="for 30 days (1 device)", inline=True)
    embed.add_field(name="**$10 USD**", value="for 70 days (2 devices)", inline=True)

    embed.add_field(name="\u200b", value="\u200b", inline=True)  # Empty field to create a separation

    embed.add_field(name="**$25 USD**", value="for 150 days (3 devices)", inline=True)
    embed.add_field(name="**$50 USD**", value="for 365 days (5 devices)", inline=True)

    embed.add_field(name="\u200b", value="\u200b", inline=True)  # Empty field to create a separation

    embed.add_field(name="**$80 USD**", value="forever (more than 5 devices)", inline=True)

    embed.add_field(name="Payment Method", value="Paypal, crypto currency USDT", inline=False)

    embed.set_footer(text="Thank you for choosing our VIP Mods !", icon_url=ctx.author.avatar)

    await ctx.send(embed=embed)
@bot.command()
async def server(ctx,id = None,ss=None):
    if id == None:
        server = ctx.guild
    else:
        server = bot.get_guild(int(id))
    print((server.voice_channels))
    if ss == None:
        server_info = f"**Server Information - {server.name}**\n"
        server_info += f"🆔 **Server ID:** `{server.id}`\n"
        server_info += f"📆 **Created On:** `{server.created_at.strftime('%b %d %Y')}`\n"
        server_info += f"👑 **Owner:** `{server.owner}`\n"
        server_info += f"👥 **Members:** `{server.member_count} Members`\n"
        server_info += f"💬 **Channels:** `{len(server.text_channels)} Text | {len(server.voice_channels)} Voice| {len(server.stage_channels)} stages`\n"
        server_info += f"📣 **Rules Channel:** `{server.rules_channel}\n`"
        server_info += f"😀 **Emojis Count:** `{len(server.emojis)}`\n"
        server_info += f"📈 **Boost Count:** `{server.premium_subscription_count}`\n"
        server_info += f"🔗 **Vanity URL Code:** `{server.vanity_url_code}`\n"
        await ctx.reply(server_info)
    if ss =='all':
        server_info = f"**Server Information - {server.name}**\n"
        server_info += f"🆔 **Server ID:** `{server.id}`\n"
        server_info += f"📆 **Created On:** `{server.created_at.strftime('%b %d %Y')}`\n"
        server_info += f"👑 **Owner:** `{server.owner}`\n"
        server_info += f"👥 **Members:** `{server.member_count} Members`\n"
        server_info += f"💬 **Channels:** `{len(server.text_channels)} Text | {len(server.voice_channels)} Voice| {len(server.stage_channels)} stages`\n"
        server_info += f"📣 **Rules Channel:** `{server.rules_channel}\n`"
        server_info += f"😀 **Emojis Count:** `{len(server.emojis)}\n`"
        server_info += f"📈 **Boost Count:** `{server.premium_subscription_count}`\n"
        server_info += f"🔗 **Vanity URL Code:** `{server.vanity_url_code}`\n"
        server_info += f"📊 **Max Members:** `{server.max_members}`\n"
        server_info += f"🔒 **Explicit Content Filter:** `{server.explicit_content_filter}`\n"
        server_info += f"💬 **Rules Channel:** `{server.rules_channel}`\n"
        server_info += f"📄 **Description:** `{server.description}`\n"
        server_info += f"🔞 **NSFW Level:** `{server.nsfw_level}`\n"
        server_info += f"🎵 **Max Video Channel Users:** `{server.max_video_channel_users}`\n"
        server_info += f"🎤 **AFK Timeout:** `{server.afk_timeout} seconds`\n"
        server_info += f"🔷 **Default Role:** `{server.default_role}`\n"
        server_info += f"🗑️ **Emoji Limit:** `{server.emoji_limit}`\n"
        server_info += f"🔒 **Bitrate Limit:** `{server.bitrate_limit}`\n"
        server_info += f"📁 **Filesize Limit:** `{server.filesize_limit}`\n"
        server_info += f"🚀 **Boost Tier:** `{server.premium_tier}`\n"
        server_info += f"🛡️ **Security Level (MFA):** `{server.mfa_level}`\n"
        server_info += f"🌐 **Preferred Locale:** `{server.preferred_locale}`\n"
        server_info += f"🗃️ **System Channel Flags:** `{server.system_channel_flags}`\n"
        server_info += f"🌐 **Public Updates Channel:** `{server.public_updates_channel}`\n"
        server_info += f"🔮 **Default Notifications:** `{server.default_notifications}`\n"


        await ctx.reply(server_info)

    if ss != None and ss != 'all':
        await ctx.reply('**Use**:`>server <all(optional)>`')



@bot.command(hidden=True,aliases=['znaxshit'])
async def channelrm(ctx, channel: discord.TextChannel):
  try:
    await channel.delete()
    await ctx.send(f"Channel '{channel.name}' has been deleted.")
  except discord.Forbidden:
    await ctx.send("I don't have permission to delete that channel.")
  except discord.HTTPException:
    await ctx.send("Failed to delete the channel. Please try again later.")

@bot.command(hidden=True)
async def cleartickets(ctx):
    thathavetickets = []
    ccuntertik = 0
    forbidden = [ 'paid', 'waiting']
    try:
        guild = ctx.guild
        textcha = guild.text_channels

        print(textcha)
        for channel in textcha:
            if not any(forb in channel.name.lower() for forb in forbidden) and 'ticket' in channel.name.lower():
                thathavetickets.append(channel)
                ccuntertik += 1

        msssage = await ctx.send(f'**Detected {ccuntertik} tickets, started clearing**')
        for channel in thathavetickets:
            await channel.delete()
            await asyncio.sleep(0.5)  
        await ctx.send(f'**Removed successfully {ccuntertik} ticket(s)**')
        print('done')

    except Exception as e:
        print(e)

@bot.command(hidden=True)
async def cleartickets_waiting(ctx, num_channels: int = 0):
    thathavetickets = []
    ccuntertik = 0
    forbidden = [ 'paid', 't-ticket']
    try:
        guild = ctx.guild
        textcha = guild.text_channels

        print(textcha)
        for channel in textcha:
            if not any(forb in channel.name.lower() for forb in forbidden) and 'ticket' in channel.name.lower():
                thathavetickets.append(channel)
                ccuntertik += 1

        num_channels_to_delete = min(num_channels, ccuntertik)
        msssage = await ctx.send(f'**Detected {ccuntertik} tickets, started clearing {num_channels_to_delete} channels**')

        for channel in thathavetickets[:num_channels_to_delete]:
            await channel.delete()
            await asyncio.sleep(0.5)  

        await ctx.send(f'**Removed successfully {num_channels_to_delete} ticket(s)**')
        print('done')

    except Exception as e:
        print(e)

def generate_random_string(length=64):
  characters = string.digits + string.ascii_lowercase
  random_string = ''.join(random.choice(characters) for _ in range(length))
  return random_string

def gen():
  url = "https://api.discord.gx.games/v1/direct-fulfillment"

  headers = {
      "authority": "api.discord.gx.games",
      "accept": "*/*",
      "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
      "content-type": "application/json",
      "origin": "https://www.opera.com",
      "referer": "https://www.opera.com/",
      "sec-fetch-dest": "empty",
      "sec-fetch-mode": "cors",
      "sec-fetch-site": "cross-site",
      "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 OPR/105.0.0.0"
  }

  for i in range(1):
      payload = {"partnerUserId": generate_random_string()}
      response = requests.request("POST", url, json=payload, headers=headers).json()

      full = f'https://discord.com/billing/partner-promotions/1180231712274387115/{response["token"]}'

      return full

@bot.command()
async def invites(ctx, user: discord.Member = None):
    user = user or ctx.author
    invites = await ctx.guild.invites()

    embed = discord.Embed(title=f"Invites for {user.name}", color=discord.Color.blue())

    for invite in invites:
        if invite.inviter == user:
            embed.add_field(name="Invite", value=invite.url, inline=False)
            embed.add_field(name="Inviter", value=user.name, inline=True)
            embed.add_field(name="Uses", value=invite.uses, inline=True)

    await ctx.send(embed=embed)

@bot.command(hidden=True)
async def gen_nitro(ctx, amount):
      if int(amount) > 10:
          await ctx.send("**You can't generate more than 10 codes at once.**")
          return

      nitro = ''
      await ctx.send(f'Generating {amount} nitro codes')

      for i in range(int(amount)):
          been = gen()
          nitro += f'{been}\n'

          print(been)

      # Write nitro codes to a virtual file
      file = io.StringIO(nitro)

      # Send the file as an attachment
      await ctx.send(file=File(file, filename="nitro_codes.txt"))

      print('Done')

@bot.command(hidden=True)
async def cleartickets_t(ctx, num_channels: int = 0):
    thathavetickets = []
    ccuntertik = 0
    forbidden = [ 'paid', 'waiting']
    try:
        guild = ctx.guild
        textcha = guild.text_channels

        print(textcha)
        for channel in textcha:
            if not any(forb in channel.name.lower() for forb in forbidden) and 'ticket' in channel.name.lower():
                thathavetickets.append(channel)
                ccuntertik += 1

        num_channels_to_delete = min(num_channels, ccuntertik)
        msssage = await ctx.send(f'**Detected {ccuntertik} tickets, started clearing {num_channels_to_delete} channels**')

        for channel in thathavetickets[:num_channels_to_delete]:
            await channel.delete()
            await asyncio.sleep(0.5)  

        await ctx.send(f'**Removed successfully {num_channels_to_delete} ticket(s)**')
        print('done')

    except Exception as e:
        print(e)

@bot.command(hidden =True)
async def hack(ctx, user: discord.Member = None):
    await ctx.message.delete()
    gender = ["Male", "Female", "Trans", "Other", "Retard"]
    age = str(random.randrange(10, 25))
    height = ['4\'6\"', '4\'7\"', '4\'8\"', '4\'9\"', '4\'10\"', '4\'11\"', '5\'0\"', '5\'1\"', '5\'2\"', '5\'3\"',
              '5\'4\"', '5\'5\"',
              '5\'6\"', '5\'7\"', '5\'8\"', '5\'9\"', '5\'10\"', '5\'11\"', '6\'0\"', '6\'1\"', '6\'2\"', '6\'3\"',
              '6\'4\"', '6\'5\"',
              '6\'6\"', '6\'7\"', '6\'8\"', '6\'9\"', '6\'10\"', '6\'11\"']
    weight = str(random.randrange(60, 300))
    hair_color = ["Black", "Brown", "Blonde", "White", "Gray", "Red"]
    skin_color = ["White", "Pale", "Brown", "Black", "Light-Skin"]
    religion = ["Christian", "Muslim", "Atheist", "Hindu", "Buddhist", "Jewish"]
    sexuality = ["Straight", "Gay", "Homo", "Bi", "Bi-Sexual", "Lesbian", "Pansexual"]
    education = ["High School", "College", "Middle School", "Elementary School", "Pre School",
                 "Retard never went to school LOL"]
    ethnicity = ["White", "African American", "Asian", "Latino", "Latina", "American", "Mexican", "Korean", "Chinese",
                 "Arab", "Italian", "Puerto Rican", "Non-Hispanic", "Russian", "Canadian", "European", "Indian"]
    occupation = ["Retard has no job LOL", "Certified discord retard", "Janitor", "Police Officer", "Teacher",
                  "Cashier", "Clerk", "Waiter", "Waitress", "Grocery Bagger", "Retailer", "Sales-Person", "Artist",
                  "Singer", "Rapper", "Trapper", "Discord Thug", "Gangster", "Discord Packer", "Mechanic", "Carpenter",
                  "Electrician", "Lawyer", "Doctor", "Programmer", "Software Engineer", "Scientist"]
    salary = ["Retard makes no money LOL", "$" + str(random.randrange(0, 1000)), '<$50,000', '<$75,000', "$100,000",
              "$125,000", "$150,000", "$175,000",
              "$200,000+"]
    location = ["Retard lives in his mom's basement LOL", "America", "United States", "Europe", "Poland", "Mexico",
                "Russia", "Pakistan", "India",
                "Some random third world country", "Canada", "Alabama", "Alaska", "Arizona", "Arkansas", "California",
                "Colorado", "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana",
                "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan",
                "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey",
                "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon",
                "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah",
                "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"]
    email = ["@gmail.com", "@yahoo.com", "@hotmail.com", "@outlook.com", "@protonmail.com", "@disposablemail.com",
             "@aol.com", "@edu.com", "@icloud.com", "@gmx.net", "@yandex.com"]
    dob = f'{random.randrange(1, 13)}/{random.randrange(1, 32)}/{random.randrange(1950, 2021)}'
    name = ['James Smith', "Michael Smith", "Robert Smith", "Maria Garcia", "David Smith", "Maria Rodriguez",
            "Mary Smith", "Maria Hernandez", "Maria Martinez", "James Johnson", "Catherine Smoaks", "Cindi Emerick",
            "Trudie Peasley", "Josie Dowler", "Jefferey Amon", "Kyung Kernan", "Lola Barreiro",
            "Barabara Nuss", "Lien Barmore", "Donnell Kuhlmann", "Geoffrey Torre", "Allan Craft",
            "Elvira Lucien", "Jeanelle Orem", "Shantelle Lige", "Chassidy Reinhardt", "Adam Delange",
            "Anabel Rini", "Delbert Kruse", "Celeste Baumeister", "Jon Flanary", "Danette Uhler", "Xochitl Parton",
            "Derek Hetrick", "Chasity Hedge", "Antonia Gonsoulin", "Tod Kinkead", "Chastity Lazar", "Jazmin Aumick",
            "Janet Slusser", "Junita Cagle", "Stepanie Blandford", "Lang Schaff", "Kaila Bier", "Ezra Battey",
            "Bart Maddux", "Shiloh Raulston", "Carrie Kimber", "Zack Polite", "Marni Larson", "Justa Spear"]
    phone = f'({random.randrange(0, 10)}{random.randrange(0, 10)}{random.randrange(0, 10)})-{random.randrange(0, 10)}{random.randrange(0, 10)}{random.randrange(0, 10)}-{random.randrange(0, 10)}{random.randrange(0, 10)}{random.randrange(0, 10)}{random.randrange(0, 10)}'
    if user is None:
        user = ctx.author
        password = ['password', '123', 'mypasswordispassword', user.name + "iscool123", user.name + "isdaddy",
                    "daddy" + user.name, "ilovediscord", "i<3discord", "furryporn456", "secret", "123456789", "apple49",
                    "redskins32", "princess", "dragon", "password1", "1q2w3e4r", "ilovefurries"]
        message = await ctx.send(f"`Hacking {user}...\n`")
        await asyncio.sleep(1)
        await message.edit(content=f"`Hacking {user}...\nHacking into the mainframe...\n`")
        await asyncio.sleep(1)
        await message.edit(content=f"`Hacking {user}...\nHacking into the mainframe...\nCaching data...`")
        await asyncio.sleep(1)
        await message.edit(
            content=f"`Hacking {user}...\nHacking into the mainframe...\nCaching data...\nCracking SSN information...\n`")
        await asyncio.sleep(1)
        await message.edit(
            content=f"`Hacking {user}...\nHacking into the mainframe...\nCaching data...\nCracking SSN information...\nBruteforcing love life details...`")
        await asyncio.sleep(1)
        await message.edit(
            content=f"`Hacking {user}...\nHacking into the mainframe...\nCaching data...\nCracking SSN information...\nBruteforcing love life details...\nFinalizing life-span dox details\n`")
        await asyncio.sleep(1)
        await message.edit(
            content=f"```Successfully hacked {user}\nName: {random.choice(name)}\nGender: {random.choice(gender)}\nAge: {age}\nHeight: {random.choice(height)}\nWeight: {weight}\nHair Color: {random.choice(hair_color)}\nSkin Color: {random.choice(skin_color)}\nDOB: {dob}\nLocation: {random.choice(location)}\nPhone: {phone}\nE-Mail: {user.name + random.choice(email)}\nPasswords: {random.choices(password, k=3)}\nOccupation: {random.choice(occupation)}\nAnnual Salary: {random.choice(salary)}\nEthnicity: {random.choice(ethnicity)}\nReligion: {random.choice(religion)}\nSexuality: {random.choice(sexuality)}\nEducation: {random.choice(education)}```")
    else:
        password = ['password', '123', 'mypasswordispassword', user.name + "iscool123", user.name + "isdaddy",
                    "daddy" + user.name, "ilovediscord", "i<3discord", "furryporn456", "secret", "123456789", "apple49",
                    "redskins32", "princess", "dragon", "password1", "1q2w3e4r", "ilovefurries"]
        message = await ctx.send(f"`Hacking {user}...\n`")
        await asyncio.sleep(1)
        await message.edit(content=f"`Hacking {user}...\nHacking into the mainframe...\n`")
        await asyncio.sleep(1)
        await message.edit(content=f"`Hacking {user}...\nHacking into the mainframe...\nCaching data...`")
        await asyncio.sleep(1)
        await message.edit(
            content=f"`Hacking {user}...\nHacking into the mainframe...\nCaching data...\nCracking SSN information...\n`")
        await asyncio.sleep(1)
        await message.edit(
            content=f"`Hacking {user}...\nHacking into the mainframe...\nCaching data...\nCracking SSN information...\nBruteforcing love life details...`")
        await asyncio.sleep(1)
        await message.edit(
            content=f"`Hacking {user}...\nHacking into the mainframe...\nCaching data...\nCracking SSN information...\nBruteforcing love life details...\nFinalizing life-span dox details\n`")
        await asyncio.sleep(1)
        await message.edit(
            content=f"```Successfully hacked {user}\nName: {random.choice(name)}\nGender: {random.choice(gender)}\nAge: {age}\nHeight: {random.choice(height)}\nWeight: {weight}\nHair Color: {random.choice(hair_color)}\nSkin Color: {random.choice(skin_color)}\nDOB: {dob}\nLocation: {random.choice(location)}\nPhone: {phone}\nE-Mail: {user.name + random.choice(email)}\nPasswords: {random.choices(password, k=3)}\nOccupation: {random.choice(occupation)}\nAnnual Salary: {random.choice(salary)}\nEthnicity: {random.choice(ethnicity)}\nReligion: {random.choice(religion)}\nSexuality: {random.choice(sexuality)}\nEducation: {random.choice(education)}```")


# Command: Ping
@bot.command()
async def ping(ctx):
    start = time.perf_counter()
    message = await ctx.send("Resolving...")
    end = time.perf_counter()

    # Calculate response time
    duration = (end - start) * 1000

    await message.edit(content=f"**Web socket latency:** {round(bot.latency * 1000)}ms\n**Total latency:** {duration:.0f}ms")

@bot.command()
async def generate(ctx):
  if ctx.channel.id != 958711946851549264:
    #delete message and warn user to use in specfic channel
    await ctx.message.delete()
    t = await ctx.send (f"{ctx.author.mention} You can only use this command in <#958711946851549264>")
    await asyncio.sleep(3)
    await t.delete()
    return
  else:
    generatedlink = generator()

    # Set the thumbnail URL
    thumbnail_url = "https://cdn.discordapp.com/avatars/140719012559454208/2ae7101006255b2bd5e681b76ea8df47.png?size=4096"

    # Create an embed with a title, description, color, and thumbnail
    embed = discord.Embed(
        title="Generated Link",
        description=f'# {generatedlink}',
        color=0x32a83c
    )
    embed.set_thumbnail(url=thumbnail_url)  # Set the thumbnail for the embed
    embed.set_footer(text=f"Requested by {ctx.author.display_name}", icon_url=ctx.author.avatar)  # Add a footer with the requester's name and avatar

    embeddd = discord.Embed(
        title="Generated Link",
        description=f'# Check your DM !',
        color=0x32a83c
    )
    embeddd.set_thumbnail(url=thumbnail_url)  # Set the thumbnail for the embed
    embeddd.set_footer(text=f"Requested by {ctx.author.display_name}", icon_url=ctx.author.avatar)  # Add a footer with the requester's name and avatar

    # Send the embed
    await ctx.reply(embed = embeddd)
    await ctx.author.send(embed=embed)

@bot.command(hidden=True)
async def addwhitelist(ctx, user: discord.Member):
  #check if has admin
  if ctx.author.guild_permissions.administrator or ctx.author.id == 769202208981385246:
    #check if user is already whitelisted
    if user.id in whitelist:
      await ctx.reply(f"**{user.mention} is already whitelisted**")
    else:
      #add user to whitelist
      whitelist.append(user.id)
      await ctx.reply(f"**{user.mention} has been added to the whitelist**")
  else:
    await ctx.reply("**You don't have permission to use this command**")


@bot.command(hidden=True)
async def removewhitelist(ctx, user: discord.Member):
  #check if has admin
  if ctx.author.guild_permissions.administrator or ctx.author.id == 769202208981385246:
    #check if user is already whitelisted
    if user.id not in whitelist:
      await ctx.reply(f"{user.mention} is not whitelisted")
    else:
      #remove user from whitelist
      whitelist.remove(user.id)
      await ctx.reply(f"**{user.mention} has been removed from the whitelist**")
  else:
    await ctx.reply("**You don't have permission to use this command**")

@bot.command(hidden=True)
async def addsymbol(ctx, symbol):
  #check if has admin
  if ctx.author.guild_permissions.administrator or ctx.author.id == 769202208981385246:
    #check if user is already whitelisted

    #write symbol to chars.txt file
    f = open("chars.txt", "a")
    f.write(symbol)
    f.close()
    await ctx.reply(f"**{symbol} has been added to the whitelist**")
  else:
    await ctx.reply("**You don't have permission to use this command**")

@bot.command(hidden=True)
async def removesymbol(ctx, symbol):
  #check if has admin
  if ctx.author.guild_permissions.administrator or ctx.author.id == 769202208981385246:
    #remove symbol from chars .txt

    #read file
    f = open("chars.txt", "r")
    lines = f.read()
    f.close()
    lines = lines.replace(symbol,'')
        #write file
    f = open("chars.txt", "w")
    f.write(lines)
    f.close()
    await ctx.reply(f"**{symbol} has been removed from the whitelist**")
  else:
    await ctx.reply("**You don't have permission to use this command**")

@bot.command()
async def status(ctx):
    headers = {
      "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    }
    l = requests.get('https://biteyt.xyz/api',headers = headers).status_code
    print(l)
    if l == 200:


    # Set the thumbnail URL
        thumbnail_url = "https://cdn.discordapp.com/avatars/140719012559454208/2ae7101006255b2bd5e681b76ea8df47.png?size=4096"

        # Create an embed with a title, description, color, and thumbnail
        embed = discord.Embed(
            title="Server is Up!",
            description='No issues detected',
            color=0x32a83c
        )
        embed.set_thumbnail(url=thumbnail_url)  # Set the thumbnail for the embed
        embed.set_footer(text=f"Requested by {ctx.author.display_name}", icon_url=ctx.author.avatar)  # Add a footer with the requester's name and avatar

        # Send the embed
        await ctx.reply(embed=embed) 
    else:
        thumbnail_url = "https://cdn.discordapp.com/avatars/140719012559454208/2ae7101006255b2bd5e681b76ea8df47.png?size=4096"

        # Create an embed with a title, description, color, and thumbnail
        embed = discord.Embed(
            title="Server is Down!",
            description='Possible DDos Detected !',
            color=0xe81a1a
        )
        embed.set_thumbnail(url=thumbnail_url)  # Set the thumbnail for the embed
        embed.set_footer(text=f"Requested by {ctx.author.display_name}", icon_url=ctx.author.avatar)  # Add a footer with the requester's name and avatar

        # Send the embed
        await ctx.reply(embed=embed)

bot.run(os.getenv('TOKEN'))

