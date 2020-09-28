import os
import configparser as cp

configFile = 'config.ini'
discordGroup = 'Discord'
tokenKey = 'discord token'
prefixKey = 'command prefix'
notificationChannelKey = 'channel id'
notificationGuildKey = 'notification guild id'
notificationRoleKey = 'notification role id'
vkGroup = 'VK'
vkLoginKey = 'vk authorization login'
vkPasswordKey = 'vk authorization password'
vkPageKey = 'vk page'


class Config:
    def __init__(self):
        self.cp = cp.ConfigParser()
        self.check_config()

    def check_config(self):
        if os.path.isfile(configFile):
            self.cp.read(configFile)
            return
        print('No config.ini file. Creating a default one.')
        self.create_config()

    def create_config(self):
        self.cp[discordGroup] = {}
        self.cp[discordGroup][tokenKey] = ''
        self.cp[discordGroup][prefixKey] = '>'
        self.cp[vkGroup] = {}
        self.cp[vkGroup][vkLoginKey] = ''
        self.cp[vkGroup][vkPasswordKey] = ''

        with open(configFile, 'w') as file:
            self.cp.write(file)

    def set(self, setting, value):
        if setting == 'channel':
            key = notificationChannelKey
            group = discordGroup
        elif setting == 'role':
            key = notificationRoleKey
            group = discordGroup
        elif setting == 'vk_page':
            key = vkPageKey
            group = vkGroup
        else:
            return False
        self.cp[group][key] = value
        with open(configFile, 'w') as file:
            self.cp.write(file)
        return True

    def clear(self, setting):
        if setting == 'channel':
            key = notificationChannelKey
            group = discordGroup
        elif setting == 'role':
            key = notificationRoleKey
            group = discordGroup
        elif setting == 'vk_page':
            key = vkPageKey
            group = vkGroup
        self.cp[group].pop(key)
        with open(configFile, 'w') as file:
            self.cp.write(file)



    @property
    def bot_token(self):
        return self.cp[discordGroup][tokenKey]

    @property
    def bot_prefix(self):
        return self.cp[discordGroup][prefixKey]

    @property
    def notification_channel(self):
        return int(self.cp[discordGroup][notificationChannelKey])

    @property
    def notification_role(self):
        return int(self.cp[discordGroup][notificationRoleKey])

    @property
    def vk_credentials(self):
        return self.cp[vkGroup][vkLoginKey], self.cp[vkGroup][vkPasswordKey]

    @property
    def vk_page_id(self):
        return self.cp[vkGroup][vkPageKey]


if __name__ == '__main__':
    config = Config()
    print(config.bot_token)




