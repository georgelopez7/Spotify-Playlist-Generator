# Creates a Spotify playlist based on a user inputted string
# -------------------------------------------------------------------------------------------------------------------#
# Imports
import nextcord
from nextcord import Interaction
from nextcord.ext import commands
from nextcord import File, ButtonStyle
from nextcord.ui import Button, View
from spotify_playlist_creation import *
# -------------------------------------------------------------------------------------------------------------------#
# Intialisng the nextcord modules
intents = nextcord.Intents.default()
intents.message_content = True

# -------------------------------------------------------------------------------------------------------------------#
# Defining the prefix for the discord commands, in this case we prefix our commands with " ! "
client = commands.Bot(command_prefix = '!',intents = intents)

# -------------------------------------------------------------------------------------------------------------------#
# The !playlist function
# This function is used to create the spotify playlist based on the user inputted string
@client.command(name = 'playlist')
# The user inputs the !playlist command along with their desired string " "
async def button_confirmation(ctx,mystr:str):
    
    # Produces the confirmation button for the user
    string = str(mystr)
    # YES Button
    yes = Button(label = 'Yes',style = ButtonStyle.blurple)
    async def one(interaction):
        
        # Send a message telling the user their playlist is being created
        await interaction.response.send_message('Creating your playlist...',ephemeral=True)

        # Used to create Spotify playlist from the spotify_playlist_creation.py file
        link, checker = creation.SpotifyPlaylistCreation(string)

        # Checks for any invalid inputs
        if checker is True:
            await interaction.followup.send('There was an invalid input!',ephemeral=True)
        # Send the link to  the user in discord
        else:
            await interaction.followup.send(f'{link}',ephemeral=True)
              
    yes.callback = one
# -------------------------------------------------------------------------------------------------------------------#
    # NO Button
    no = Button(label = 'No',style = ButtonStyle.blurple)
    async def two(interaction):
        await interaction.response.send_message('Please try again! (Ensure you have your message within ' + '" "' + ')')

    no.callback = two

    myview = View(timeout=180)
    myview.add_item(yes)
    myview.add_item(no)
    
    # Confirmation message for the user, sent before the playlist is created
    m_id = await ctx.send(f'Would you like to make a playlist with: \n"{string}"', view=myview)
# -------------------------------------------------------------------------------------------------------------------#   
if __name__ == '__main__':
    client.run('discord-token-here')

