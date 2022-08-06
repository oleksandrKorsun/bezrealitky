import time


def test_bezrealitky(app):
    app.realitka.openUrl("https://www.bezrealitky.cz/moje-bezrealitky/hlidaci-pes")
    app.realitka.logIn('bersh92@gmail.com','xuWveLiU4@Tivy9')
    app.realitka.click_on_dog_button_and_load_flats()
    app.realitka.find_flats()