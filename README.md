# VkToDis
A Discord bot written on python using discord.py wrapper that sends post from VK to Discord
### Installation
1. Clone repository ```git clone https://github.com/JustTrott/VkToDis.git```
2. install requirements ```pip install -r requirements.txt```
3. Run ```bot.py``` file. You will catch an error about creating the ```config.ini``` file in the directory.
4. Enter your Discord bot token, prefix, VK authorization login and password in ```config.ini``` file.
5. Run ```bot.py```
WARNING: All the commands work only in server chats and do not in DMs
### Commands:
<details>
 <summary><b>send_post</b>:</summary>
  There are few optional arguments for this command:
 
  - *post_id* which is set to **1** by default. This means that by default the most recent post on the wall will be sent
  
  Usage example:```send_post 3```
  
  This command will send the third post from the wall
  
  - *vk_page_id* which is set to **None** by default. You can change this setting using command ```set channel #channel``` (Check out **set** command for more info)
  
  Usage example: ```send_post 1 durov```
  
  This command will send the first post from the ***vk.com/durov*** wall
  
  **Note** that you **must** write **post_id** before **vk_page_id** otherwise command just will not work
</details>
<details>
 <summary><b>set</b>:</summary>
  There are two required arguments for this command:
  
  - ***setting*** is argument that represents the setting that you are going to change. It can take on these values: channel, role, vk_page
  
  1. *channel* setting is the one you use when you want to change the default channel to which the post will be sent. By default this setting is set to the channel, where **send_post** command is called from
  
  2. *role* setting is the one you use when you want to change the default role that will be mentioned when the post is submitted. By default this setting is set to **None**
  
  3. *vk_page* setting is the one you use when you want to change the default VK page from which posts are retrieved. By default this setting is set to **None**
  
  - ***value*** is argument that represents the value you assign to the setting.
  
  1. For the *channel* setting you need to **mention** the channel that you need.
  
  Usage example: ```set channel #text-channel```
  
  2. For the *role* setting you need to **mention** the role that you need.
  
  Usage example: ```set role @Notifications```
  
  3. For the *vk_page* setting you need to type page's id or short link.
  
  Usage example: ```set vk_page durov``` ```set vk_page id1``` ```set vk_page club1```
</details>
