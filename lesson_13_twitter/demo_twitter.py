import asyncio
import twitter

import sys
from loguru import logger

logger.remove()
logger.add(sys.stdout, level="INFO")
logger.enable("twitter")


proxy = 'http://TS4hXHJS:CZArvuze@45.147.1.211:64392'

my_twitter_id = 1801148079321542656
elonmusk_twitter_id = 44196397


async def main():
    twitter_client: twitter.Client

    # twitter_account = twitter.Account(auth_token="bab3c66c5a550225732862b21919cec4ab5188e2")

    twitter_account = twitter.Account(
        auth_token='106aab0df134bcaecb5943094874673eccaf81fe',
        username='PaytonWatk89533',
        password='hcMscB452064',
        email='bayuk5392prots9@hotmail.com',
        totp_secret='HTTY27L2LJNYP4CV'
    )

    async with twitter.Client(twitter_account, proxy=proxy) as twitter_client:
        print(f"Logged in as @{twitter_account.username} (id={twitter_account.id})")

        '''
        Внетренний метод для обращения к API Twitter
        Пытаемся отправить HTTP запрос по переданному URL адресу
        Если ловим ошибку AccountLocked, то пытаемся разблокировать аккаунт 
        (необходимо передать auto_unlock=True в данный метод и установить capsolver_api_key в Client)
        Если ловим ошибку BadAccountToken, то пытаемся перелогиниться в аккаунт
        (необходимо установить auto_relogin=True в Client, а также передать password и email или username в Account)
        '''
        # print(await twitter_client.request())

        '''
        Метод ищет информацию о twitter аккаунте по переданному username и возвращает модель Account 
        '''
        # print(await twitter_client.request_user_by_username(username='elonmusk'))
        # print((await twitter_client.request_user_by_username(username='elonmusk')).json())

        '''
        Метод обновляет информацию о client.account с помощью метода request_user_by_username()
        (если у объекта не установлено поле client.account.username, 
        то сначала делается запрос на обновление этого поля)
        '''
        # await twitter_client.update_account_info()

        '''
        Метод Client.establish_status() устанавливает статус аккаунта. 
        Также статус аккаунта может изменить любое взаимодействие с Twitter. 
        Поэтому, во время работы может внезапно быть вызвано исключение семейства twitter.errors.BadAccount.
        В случае успеха, устанавливается статус GOOD (при создании Account устанавливается статус UNKNOWN)
        '''
        # await twitter_client.establish_status()

        '''
        Метод, который вызывается при создании клиента через асинхронный менеджер контекста
        Если в Client стоит update_account_info_on_startup=True, 
        то вызовутся методы update_account_info() и establish_status()
        '''
        # print(await twitter_client.on_startup())

        '''
        Метод ищет информацию о twitter аккаунте по переданному user_id и возвращает модель Account 
        '''
        # print(await twitter_client.request_user_by_id(user_id=elonmusk_twitter_id))

        '''
        Метод ищет информацию о twitter аккаунтах по переданным user_ids и возвращает модели Account 
        '''
        # print(await twitter_client.request_users_by_ids(user_ids=(elonmusk_twitter_id, my_twitter_id)))

        '''
        Метод позволяет подписаться на аккаунт по user_id. Возвращает bool
        '''
        # print(await twitter_client.follow(user_id=elonmusk_twitter_id))

        '''
        Метод позволяет отписаться от аккаунта по user_id. Возвращает bool
        '''
        # print(await twitter_client.unfollow(user_id=elonmusk_twitter_id))

        '''
        Метод позволяет поставить like на твитт по tweet_id. Возвращает bool
        '''
        # print(await twitter_client.like(tweet_id=1810808931486421311))

        '''
        Метод позволяет убрать like с твитта по tweet_id. Возвращает bool
        '''
        # print(await twitter_client.unlike(tweet_id=1810808931486421311))

        '''
        Метод позволяет репостнуть твитт tweet_id. Возвращает модель Tweet. 
        Если твитт уже репостнули, метод просто возвращает модель Tweet
        '''
        # print(await twitter_client.repost(tweet_id=1810808931486421311))

        '''
        Метод позволяет твиттнуть переданный текст, а также добавить медиа контент по media_id.
        Возвращает модель Tweet 
        '''
        # print(await twitter_client.tweet(text='My first tweet!!', media_id=1811064390596317190))

        '''
        Метод позволяет закрепить твитт по tweet_id. Возвращает bool 
        '''
        # print(await twitter_client.pin_tweet(tweet_id=1811062127668420628))

        '''
        Метод позволяет удалить твитт по tweet_id. Возвращает bool 
        '''
        # print(await twitter_client.delete_tweet(tweet_id=1811062127668420628))

        '''
        Метод позволяет сделать replay на твитт, а также добавить текст и медиа контент по media_id.
        Возвращает модель Tweet 
        '''
        # print(await twitter_client.reply(tweet_id=1802409584189194530, text='jajajaj'))

        '''
        Метод позволяет сделать quote на твитт, а также добавить текст и медиа контент по media_id.
        Возвращает модель Tweet 
        '''
        # print(await twitter_client.quote(
        #     tweet_url='https://x.com/NASA/status/1802366777575297109',
        #     text='my text'
        # ))

        '''
        Метод позволяет получить список подписчиков по user_id (максимум 70)
        Возвращает модель list[User] 
        '''
        # print(await twitter_client.request_followers(user_id=elonmusk_twitter_id))

        '''
        Метод позволяет получить список подписок по user_id (максимум 70)
        Возвращает модель list[User] 
        '''
        # print(await twitter_client.request_followings(user_id=elonmusk_twitter_id))

        '''
        Метод позволяет получить информацию о твитте по tweet_id. Возвращает модель Tweet
        '''
        # print(await twitter_client.request_tweet(tweet_id=1811062757220929705))

        '''
        Метод позволяет спарсить последние твитты у пользователя по user_id. 
        Возвращает list[Tweet]
        '''
        # print(await twitter_client.request_tweets(user_id=elonmusk_twitter_id))

        '''
        Метод позволяет загрузить медиаконтент на сервер твиттер 
        Возвращает модель Media
        '''
        # with open('avatar.jpg', 'rb') as f:
        #     data = f.read()
        #     print(data)
        #     print(await twitter_client.upload_image(image=data))  # 1811064294173462533
        # with open('banner.jpeg', 'rb') as f:
        #     data = f.read()
        #     print(await twitter_client.upload_image(image=data))  # 1811064390596317190

        '''
        Метод позволяет обновить аватарку пользователя 
        Возвращает ссылку на аватарку
        '''
        # print(await twitter_client.update_profile_avatar(media_id=1811064294173462533))

        '''
        Метод позволяет обновить баннер пользователя 
        Возвращает ссылку на баннер
        '''
        # print(await twitter_client.update_profile_banner(media_id=1811064390596317190))

        '''
        Метод позволяет обновить username
        Возвращает bool
        '''
        # print(await twitter_client.change_username(username='PaytonWatk89533'))

        '''
        Метод позволяет обновить имя пользователя, описание, локацию и вебсайт профиля
        Возвращает bool
        '''
        # print(await twitter_client.update_profile(
        #     name='Payton Watk',
        #     description='Cool guy',
        #     location='Unknown city',
        #     website='mywebsite.com'
        # ))

        '''
        Метод позволяет обновить дату рождения
        Возвращает bool
        
        !! метод не работает
        Текущий запрос: 
        
        POST: https://api.x.com/1.1/account/update_profile.json
        Payload:
        {
            "birthdate_day": 1
            "birthdate_month": 1
            "birthdate_year": 2000
            "birthdate_visibility": "public"
            "birthdate_year_visibility": "public"
            "displayNameMaxLength": 50
            "url": "http://mywebsite.com"
            "name": "Kron Morgan"
            "description": "Cool guy"
            "location": "Unknown city2"
        }
        '''
        # print(await twitter_client.update_birthdate(
        #     day=2,
        #     month=1,
        #     year=2000,
        #     visibility='self',
        #     year_visibility='self'
        # ))

        '''
        Если account.status == "LOCKED", то метод пытается разблокировать аккаунт
        Метод вызывается внутри client.request()
        Чтобы метод начал выполнение, нужно установить client.capsolver_api_key, 
        а также передать auto_unlock=True в метод request 
        '''
        # print(await twitter_client.unlock())

        '''
        Метод позволяет проголосовать в опросе 
        Метод принимает tweet_id, card_id, и номер ответа
        card_id можно достать из информации о твитте
        Метод возвращает dict
        '''
        # tweet_id = 1811071203655794813
        # tweet = await twitter_client.request_tweet(tweet_id=tweet_id)
        # card_id = tweet.raw_data['card']['rest_id'].split('://')[1]
        # print(await twitter_client.vote(
        #     tweet_id=tweet_id,
        #     card_id=card_id,
        #     choice_number=2
        # ))

        '''
        Метод позволяет отправлять сообщения (можно отправить самому себе)
        Возвращает dict
        '''
        # print(await twitter_client.send_message(
        #     user_id=1801134262382411776,
        #     text='hello'
        # ))

        '''
        Позволяет отправить сообщение в чат
        Возвращает dict
        '''
        # print(await twitter_client.send_message_to_conversation(
        #     conversation_id='1801134262382411776-1801148079321542656',
        #     text='GM'
        # ))

        '''
        Метод позволяет получить все сообщения
        Возвращает dict
        '''
        # print(await twitter_client.request_messages())

        '''
        Метод позволяет поменять пароль от твиттер аккаунта
        Для работы метода необходимо ввести старый пароль аккаунта в модель Account
        
        !! При смене пароля, обновляется auth_token !!
        
        Если обновился auth_token утерян, то нужно заново залогиниться в аккаунт и получить auth_token
        Для логина в аккаунт необходимо указать username, email, password и totp_secret в модели Account и сделать login
        '''
        # print(await twitter_client.change_password(
        #     password='hcMscB452064'
        # ))
        # print(f'new auth_token is: {twitter_client.account.auth_token}')

        '''
        Метод позволяет сделать login в аккаунт
        Для логина в аккаунт необходимо указать username, email, password и totp_secret в модели Account и сделать login
        '''
        # twitter_account = twitter.Account(
        #     username='trent_bish56112',
        #     password='Hl8rEH211034',
        #     email='humid6453jamy@hotmail.com',
        #     totp_secret='7POFNLPN43LHLRRS'
        # )
        # twitter_client = twitter.Client(twitter_account, proxy=proxy)
        # print(await twitter_client.relogin())
        # print(f'new auth_token is: {twitter_client.account.auth_token}')

        '''
        В отличии от метода relogin, метод login проверяет наличие auth_token
        Если есть auth_token, то проверяется статус аккаунта через establish_status 
            и если с аккаунтом всё впорядке, ничего не происходит 
        Если нет auth_token, то вызывается метод relogin
        
        Для работы метода необходимо указать параметры необходимые методы relogin
        '''
        # await twitter_client.login()
        # print(f'auth_token is: {twitter_client.account.auth_token}')

        '''
        Метод проверяет установлена ли на аккаунте защита через totp (Time-based one-time Password algorithm)
        Возвращает bool
        '''
        # print(await twitter_client.totp_is_enabled())
        # twitter_account = twitter.Account(
        #     totp_secret='NN6REWPK2OMJTRLI'
        # )
        # print(twitter_account.get_totp_code())

        '''
        Метод позволяет установить защиту totp, если она еще не установлена 
        Для работы метода необходимо установить password в модель Account
        
        !! Метод не возвращает totp_secret, а просто сохраняет его в модель Account.totp_secret (не забудьте сохранить)
        '''
        # print(await twitter_client.enable_totp())
        # print(twitter_account.totp_secret)

        '''
        Метод позволяет обновить backup_code (используется, если не подошел ключ Account.totp_secret
        !! Метод не возвращает backup_code, а просто сохраняет его в модель Account.backup_code (не забудьте сохранить)
        '''
        # print(twitter_account.backup_code)
        # print(await twitter_client.update_backup_code())
        # print(twitter_account.backup_code)


if __name__ == "__main__":
    asyncio.run(main())
