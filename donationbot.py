import discord
import mysql.connector
from discord.ext import commands
from discord.utils import get
from discord.ext.commands import Bot
from datetime import datetime

bot = commands.Bot(command_prefix="!")

mydb = mysql.connector.connect(
    host="localhost",
    user="donationbot",
    password="PUTPASSHERE",
    database="donationbot"
)

def add_donation(user_id, username, amount):
    cursor = mydb.cursor()
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    sql = "INSERT INTO donations (uid, username, amount, date) VALUES (%s, %s, %s, %s)"
    val = (user_id, username, amount, now)
    cursor.execute(sql, val)
    mydb.commit()
    cursor.close()

@bot.command(name='donate')
async def donate(ctx, user: discord.Member, amount: float):
    if "Management" in [role.name for role in ctx.author.roles]:
        add_donation(user.id, user.name, amount)
        await ctx.send(f"Thank you for the donation of {amount} from {user.display_name}!")
    else:
        await ctx.send("You must be in the Management role to enter donations.")

@bot.command()
async def donations(ctx):
    cursor = mydb.cursor()
    sql = "SELECT SUM(amount) FROM donations WHERE uid = %s"
    val = (ctx.author.id,)
    cursor.execute(sql, val)
    result = cursor.fetchone()
    cursor.close()
    total_donated = result[0] if result[0] else 0
    await ctx.send(f"You have donated a total of {total_donated}.")

@bot.command()
async def my_donations(ctx):
    cursor = mydb.cursor()
    sql = "SELECT SUM(amount) FROM donations WHERE uid = %s"
    val = (ctx.author.id,)
    cursor.execute(sql, val)
    result = cursor.fetchone()
    cursor.close()
    total_donated = result[0] if result[0] else 0
    await ctx.send(f"You have donated a total of {total_donated}.")

bot.run("PUT SECRET HERE")
