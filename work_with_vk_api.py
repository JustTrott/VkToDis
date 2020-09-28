import vk_api

class PostFetcher:
    def __init__(self, page_id, vk_login, vk_password):
        self.login = vk_login
        self.password = vk_password
        self.page_id = page_id
        self._profile = None

    def connect_to_vk(self):
        vk_session = vk_api.VkApi(self.login, self.password)
        try:
            vk_session.auth(token_only=True)
        except vk_api.AuthError as error_msg:
            print(error_msg)
            return None
        else:
            if self._profile is None:
                self._profile = self.get_profile_info(vk_session)
        return vk_session

    def get_post(self, offset):
        vk_session = self.connect_to_vk()
        if vk_session is None or self._profile is None:
            return None
        params = {
            'owner_id' : self._profile.id,
            'count' : 1,
            'offset' : offset
        }
        post = vk_session.method('wall.get', params)
        text = post['items'][0]['text']
        attachments = post['items'][0]['attachments']
        image_url = None
        for attachment in attachments:
            if attachment['type'] == 'photo':
                image_url = attachment['photo']['sizes'][-1]['url']
        post_id = post['items'][0]['id']
        profile = self._profile
        url = f'https://vk.com/{profile.screen_name}?w=wall{profile.id}_{post_id}'
        return text, image_url, url

    def get_profile_info(self, vk_session):
        if vk_session is None:
            return None
        params = {
            'user_ids' : self.page_id,
            'fields' : 'screen_name, first_name, last_name, photo_100'
        }
        try:
            user = vk_session.method('users.get', params)
        except:
            params = {
                'group_id' : self.page_id,
                'fields' : 'screen_name, name, photo_100'
            }
            try:
                user = vk_session.method('groups.getById', params)
            except:
                return None
            else:
                multiplier = -1
                name = user[0]['name']
        else:
            multiplier = 1
            name = user[0]['first_name'] + ' ' + user[0]['last_name']
        profile = self.Profile(user[0]['id']*multiplier, user[0]['screen_name'], name, user[0]['photo_100'])
        return profile

    @property
    def profile(self):
        return self._profile


    class Profile:
        def __init__(self, profile_id, screen_name, full_name, avatar_url):
            self._id = profile_id
            self._screen_name = screen_name
            self._full_name = full_name
            self._avatar_url = avatar_url

        @property
        def id(self):
            return self._id

        @property
        def screen_name(self):
            return self._screen_name

        @property
        def full_name(self):
            return self._full_name

        @property
        def avatar_url(self):
            return self._avatar_url
