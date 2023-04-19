from helpers.telegramBotHelper import TelegramBotHelper

telegramBot = TelegramBotHelper()


def test_bezrealitky(app):
    try:
        app.realitka.openUrl("https://www.bezrealitky.cz/moje-bezrealitky/hlidaci-pes")
        app.realitka.logIn('ivan.bedevelsky92@seznam.cz', 'ivan06061989')
        app.realitka.click_on_dog_button_and_load_flats()
        app.realitka.find_flats()
    except:
        telegramBot.send_message(248932976, '!!! ERROR test_bezrealitky WAS FAILED !!!')
        app.utils.takeScreenshot()
        telegramBot.send_photo(248932976, photo=open(app.utils.getPathToScreenshot(), 'rb'))
        app.utils.deleteAllScreenshots()