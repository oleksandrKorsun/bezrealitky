from helpers.telegramBotHelper import TelegramBotHelper

telegramBot = TelegramBotHelper()



def test_check_new_messages(app):
    try:
        app.realitka.openUrl("https://www.bezrealitky.cz/moje-bezrealitky/hlidaci-pes")
        app.realitka.logIn('ivan.bedevelsky92@seznam.cz', 'ivan06061989')
        app.realitka.check_if_new_messages_present()
    except:
        telegramBot.send_message(248932976, '!!! ERROR test_check_new_messages WAS FAILED !!!')