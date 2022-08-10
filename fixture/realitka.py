import time

from helpers.dbHelper import DbHelper
from helpers.telegramBotHelper import TelegramBotHelper


class RealitkaHelper:
    telegramBot = TelegramBotHelper()
    db_id = DbHelper("FLATS", "list_of_sent_ids")

    NewMessageIcon = "//span[text()='nepřečtené']"
    MyAccountIconButton = 'div[class^="d-none d-md"] img[alt="Oleksandr Korsun"]'
    NoItemsFoundMessage = "//p[contains(text(), 'Tomuto hledání neodpovídají žádné inzeráty')]"
    PostIsNotAvailable = "//h1[contains(text(), 'Inzerát již není v nabídce')]"
    maximum_price_of_flat = "16"
    AcceptCookiesButton = 'button[id="CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"]'
    LogInAndMenuButtons = 'div[class="d-none d-md-inline-flex btn-group"] button[class="Header_headerButton__yH0rH btn-sm btn btn-outline-dark"]'
    UserNameInputField = 'div[role="dialog"] input[id="username"]'
    PasswordInputField = 'div[role="dialog"] div[class="input-group"] input[id="password"]'
    LogInButton = 'div[role="dialog"] button[type="submit"]'
    NacistDalsiButton = "//button[contains(text(), 'Načíst další')]"
    LIST_OF_FLATS = "article[class^='PropertyCard_propertyCard']"
    PRICE_OF_THE_FLAT = 'div[class="col-xxl-5 col-lg-6 col-md-7"] strong[class="h4 fw-bold"]'
    DOG_BUTTON = "//span[contains(text(), 'Hlídací pes')]"
    ID_NUMBER_OF_THE_FLAT = "section.box.Section_section___TusU.section.mb-5.mb-lg-10 > div > div:nth-child(1) > table > tbody > tr:nth-child(1) > td"
    LoadingSpinner = 'div[class="spinner-border text-green"]'
    SuccessLogInMessage = "//div[contains(text(), 'Přihlášení proběhlo úspěšně')]"
    ContactOwnerButton = '//div[@class="box d-none d-md-block"]//button[contains(text(), "Kontaktovat majitele")]'
    MessageInputField = 'textarea[id="message"]'
    SendMessageButton = '//button[contains(text(), "Poslat zprávu")]'
    SuccessMessageText = '//h3[contains(text(), "Vaše zpráva byla úspěšně odeslána!")]'
    CloseMessageWindow = 'button[aria-label="Zavřít"]'
    TextToSend = "Dobry den,\n\nVelmi mně zaujala vase nabídka nemovitosti, Ja by chtěl přijet na prohlídku, a připadne tenhle byt pronajmout. Par slov o nás, my jsme manželé, původem z Ukrajiny, v Praze žijeme už 10 let nekoukací a nemáme domácí zvířata. Hledáme byt pro dlouhodobý pronájem na 2 a vice let, pracujeme v IT, ja pracují na pozici asistenta viceprezidenta v oboru programování Pražského oddělení pro velkou mezinárodní banku (pokud by byla potřeba můžu to potvrdit potvrzením z práce). Je nam 30 let a 28 let. Prosím o zpětnou vazbu ohledně prohlídky. Tel. Číslo: 770-677-525.\n\nS pozdravem\nOleksandr Korsun"

    def __init__(self, app):
        self.app = app
        self.step = self.app.step
        self.wd = self.app.wd

    def openUrl(self, url):
        self.wd.get(url)

    def logIn(self, username, password):
        self.step.click_on_element(self.AcceptCookiesButton)
        self.step.get_list_of_elements(self.LogInAndMenuButtons)[0].click()
        self.step.input_text(self.UserNameInputField, username)
        self.step.input_text(self.PasswordInputField, password)
        self.step.click_on_element(self.LogInButton)
        self.step.specified_element_is_present(self.SuccessLogInMessage, 5)
        time.sleep(2)

    def find_flats(self):
        if self.step.specified_element_is_present(self.NoItemsFoundMessage, time=2) == False:
            list_of_elements = len(self.step.get_list_of_elements(self.LIST_OF_FLATS))
            for element in range(list_of_elements):
                self.wd.execute_script(
                    "arguments[0].scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'start' });", self.step.get_list_of_elements(self.LIST_OF_FLATS)[element])
                time.sleep(2)
                self.step.get_list_of_elements(self.LIST_OF_FLATS)[element].click()
                self.step.specified_element_is_not_present(self.LoadingSpinner, 5)
                if self.step.specified_element_is_present(self.PostIsNotAvailable, time=1) == True:
                    self.click_on_dog_button_and_load_flats()
                elif float(self.step.get_element_text(self.PRICE_OF_THE_FLAT).split(' ')[0]) <= float(self.maximum_price_of_flat):
                    if self.db_id.check_value_in_db({"id": self.get_flat_description_id()}) == False:
                        self.send_message_to_owner(self.TextToSend)
                        self.db_id.insert_one({"id": self.get_flat_description_id()})
                        self.telegramBot.send_message(248932976, str(self.wd.current_url))
                    self.click_on_dog_button_and_load_flats()
                else:
                    self.click_on_dog_button_and_load_flats()
                list_of_elements = list_of_elements - 1
            self.db_id.close_connection()

    def click_on_dog_button_and_load_flats(self):
        self.step.click_on_element(self.DOG_BUTTON)
        self.load_all_flats_list()

    def check_if_new_messages_present(self):
        self.step.click_on_element(self.MyAccountIconButton)
        if self.step.specified_element_is_present(self.NewMessageIcon, time=4) == True:
            self.telegramBot.send_message(248932976, "!!! You Received a new message !!!")

    def load_all_flats_list(self):
        time.sleep(1)
        self.step.specified_element_is_not_present(self.LoadingSpinner, 5)
        time.sleep(1)
        if self.step.specified_element_is_present(self.NacistDalsiButton, time=1) == True:
            while self.step.specified_element_is_present(self.NacistDalsiButton, time=1) == True:
                self.step.click_on_element(self.NacistDalsiButton, scrollInToView=True)
                time.sleep(1)

    def get_flat_description_id(self):
        result = self.step.get_element_text(self.ID_NUMBER_OF_THE_FLAT)
        return result

    def check_flat_price(self):
        price = self.step.get_element_text(self.PRICE_OF_THE_FLAT)
        if "+" in price:
            price_new = price.split(' ')
            actual_price = float(price_new[0]) + float(price_new[3])
        else:
            price_new = price.split(' ')
            actual_price = float(price_new[0])
        return actual_price

    def send_message_to_owner(self, text):
        self.step.click_on_element(self.ContactOwnerButton, scrollInToView=True)
        time.sleep(2)
        self.step.input_text(self.MessageInputField, text)
        self.step.click_on_element(self.SendMessageButton, scrollInToView=True)
        time.sleep(1)
        self.step.specified_element_is_present(self.SuccessMessageText, time=5)
        self.step.click_on_element(self.CloseMessageWindow, scrollInToView=True)
        time.sleep(1)
