from datetime import datetime


def test_bezrealitky(app):
    print('start')
    app.realitka.openUrl("https://www.bezrealitky.cz/moje-bezrealitky/hlidaci-pes")
    app.realitka.logIn('bersh92@gmail.com','xuWveLiU4@Tivy9')
    app.realitka.click_on_dog_button_and_load_flats()
    app.realitka.find_flats()
    print('end')

# def test_bezrealitky(app):
#     try:
#         print('start')
#         app.realitka.openUrl("https://www.bezrealitky.cz/moje-bezrealitky/hlidaci-pes")
#         app.realitka.logIn('bersh92@gmail.com','xuWveLiU4@Tivy9')
#         app.realitka.click_on_dog_button_and_load_flats()
#         app.realitka.find_flats()
#     except Exception as e:
#         print (e)
#         now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
#         app.wd.get_screenshot_as_file('screenshot-%s.png' % now)