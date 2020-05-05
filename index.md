# RPGBot
A simple Discord that emulates a RPG.
## Features
* Character Creation with 5 classes, custom names and different stats.
* Reaction based help menu.
* Levelling.
* Earning gold and items.

## Command Help
All these commands require the prefix "rpg" behind them:

() - Optional Arguments, {} - Required Arguments
* help
  * This will show the reaction based help command.
* guild
  * create
    * Make a private/public guild (costs 10000 gold)
  * join
    * Join a guild. If the guild is private, an application to join the guild will be sent.
  * list
    * List the top 10 guilds in order of how many members they have.
  * deposit {amount}
    * Deposit {amount} gold into the guild bank.
  * withdraw {amount}
    * Withdraw {amount} gold from the guild bank.
  * balance
    * Shows how much gold is in the guild bank.
  * leave
    * Leaves your current guild.
  * applications
    * Shows all applications to join your guild. (Can only be run by the guild leader)
* inv (mention)
  * View all the items in your (or whoever you mentioned) inventory.
* delete
  * Deletes your character. **THIS CHANGE IS IRREVERSIBLE**
* profile
  * Show your profile in an image.
* message {mention}
  * Sends a message to whoever you mentioned.
* messages
  * Shows all of your current messages.
* messageClear
  * Clears all of your current messages. **THIS CANNOT BE UNDONE**
* explore
  * Explore and either fight something, find an item or get some gold/xp.
* equip {item}
  * Equip the specified item.
* unequip {item}
  * Unequip the specified item.

### Invite Link
[Invite Link](https://discordapp.com/oauth2/authorize?client_id=702276038314688593&permissions=336055360&scope=bot)
### Support Server
[Invite to Server](https://discord.gg/NWdCX57)
