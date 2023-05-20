import time

from helpers.dbHelper import DbHelper
from helpers.telegramBotHelper import TelegramBotHelper


class RealitkaHelper:
    price_of_flat = ''
    price_of_utilities = ''
    price_of_deposit = ''
    maximum_deposit = ''
    conditions = None

    telegramBot = TelegramBotHelper()
    db_id = DbHelper("FLATS", "list_of_sent_ids")

    NewMessageIcon = "//span[text()='nepřečtené']"
    MyAccountIconButton = 'div [role="toolbar"] span[class*="Avatar_avatar"]'
    NoItemsFoundMessage = "//p[contains(text(), 'Tomuto hledání neodpovídají žádné inzeráty')]"
    PostIsNotAvailable = "//h1[contains(text(), 'Inzerát již není v nabídce')]"
    StranceChybiStrechaText = "//h1[contains(text(), 'Téhle stránce chybí střecha nad hlavou')]"
    maximum_price_of_flat = "15500"
    AcceptCookiesButton = 'button[id="CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"]'
    LogInAndMenuButtons = 'div[class="d-none d-md-inline-flex btn-group"] button[class="Header_headerButton__yH0rH btn-sm btn btn-outline-dark"]'
    UserNameInputField = '#username'
    PasswordInputField = '#password'
    LogInButton = 'button[type="submit"]'
    NacistDalsiButton = "//button[contains(text(), 'Načíst další')]"
    LIST_OF_FLATS = "article[class^='PropertyCard_propertyCard']"
    PRICE_OF_THE_FLAT = 'div[class*="StickyBox_stickyBox_"] strong[class="h4 fw-bold"]'
    PRICE_OF_UTILITIES = 'div[class*="StickyBox_stickyBox_"] div[class="justify-content-between mb-2 row"] strong[class="text-body fw-bold"]'
    PRICE_OF_DEPOSIT = 'div[class*="StickyBox_stickyBox_"] div[class="justify-content-between row"] strong[class="text-body fw-bold"]'
    DOG_BUTTON = "//span[contains(text(), 'Hlídací pes')]"
    ID_NUMBER_OF_THE_FLAT = "section.box.Section_section___TusU.section.mb-5.mb-lg-10 > div > div:nth-child(1) > table > tbody > tr:nth-child(1) > td"
    LoadingSpinner = 'div[class="spinner-border text-green"]'
    SuccessLogInMessage = "//div[contains(text(), 'Přihlášení proběhlo úspěšně')]"
    ContactOwnerButton = '//*[@id="__next"]/main/div[2]/section/div/div[1]/div[2]/div[1]/p/button'
    MessageInputField = 'textarea[id="message"]'
    SendMessageButton = '//button[contains(text(), "Poslat zprávu")]'
    SuccessMessageText = '//h3[contains(text(), "Vaše zpráva byla úspěšně odeslána!")]'
    CloseMessageWindow = 'button[aria-label="Zavřít"]'
    zpravyButton = "//span[text()='Zprávy']"
    newMessageIcon = 'span[class="Badge_badge__YL9Gr Badge_badge--lg__vTcCz badge bg-primary"]'
    TextToSend = "Dobry den,\n\nVelmi mně zaujala vaše nabídka nemovitosti, Rád bych přijet na prohlídku, a připadne tenhle byt chtěl pronajmout. Pár slov o mně, jsem původem z Ukrajiny, v Praze žiju už dlouhodobe, jsem nekuřák a nemám domácí zvířata. Hledám byt pro dlouhodobý pronájem, pacuji Programatorem v oboru IT. Prosím o zpětnou vazbu ohledně prohlídky. Tel. Číslo: 770-677-525.\n\nS pozdravem\nIvan Bedevelsky"

    def __init__(self, app):
        self.app = app
        self.step = self.app.step
        self.wd = self.app.wd

    def openUrl(self, url):
        self.wd.get(url)

    def logIn(self, username, password):
        self.step.click_on_element(self.AcceptCookiesButton)
        # self.step.get_list_of_elements(self.LogInAndMenuButtons)[0].click()
        self.step.input_text(self.UserNameInputField, username)
        self.step.input_text(self.PasswordInputField, password)
        self.step.click_on_element(self.LogInButton)
        self.step.specified_element_is_present(self.SuccessLogInMessage, 5)
        self.step.specified_element_is_not_present(self.SuccessLogInMessage, 6)

    def find_flats(self):
        if self.step.specified_element_is_present(self.NoItemsFoundMessage, time=2) == False:
            list_of_elements = len(self.step.get_list_of_elements(self.LIST_OF_FLATS))
            for element in range(list_of_elements):
                self.conditions = None
                self.wd.execute_script(
                    "arguments[0].scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'start' });", self.step.get_list_of_elements(self.LIST_OF_FLATS)[element])
                time.sleep(2)
                self.step.get_list_of_elements(self.LIST_OF_FLATS)[element].click()
                self.step.specified_element_is_not_present(self.LoadingSpinner, 5)
                if self.step.specified_element_is_present(self.PostIsNotAvailable, time=1) == True or self.step.specified_element_is_present(self.StranceChybiStrechaText, time=1) == True:
                    self.click_on_dog_button_and_load_flats()
                try:
                    self.price_of_flat = int(self.step.get_element_text(self.PRICE_OF_THE_FLAT).rsplit(' ', 1)[0].replace(" ", ""))
                    self.price_of_utilities = int(self.step.get_element_text(self.PRICE_OF_UTILITIES).rsplit(' ', 1)[0].replace(" ", ""))
                    self.price_of_deposit = int(self.step.get_element_text(self.PRICE_OF_DEPOSIT).rsplit(' ', 1)[0].replace(" ", ""))
                    self.maximum_deposit = int( self.price_of_flat / 2 + self.price_of_flat)
                    if self.price_of_flat + self.price_of_utilities <= int(self.maximum_price_of_flat) and self.price_of_deposit <= self.maximum_deposit:
                        self.conditions = True
                except:
                    self.click_on_dog_button_and_load_flats()
                if self.conditions:
                    if self.db_id.check_value_in_db({"id": self.get_flat_description_id()}) == False:
                        self.send_message_to_owner(self.TextToSend)
                        self.db_id.insert_one({"id": self.get_flat_description_id()})
                        self.telegramBot.send_message(-877986264, str(self.wd.current_url))
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
        self.step.specified_element_is_not_present(self.LoadingSpinner, 5)
        time.sleep(1)
        if self.step.specified_element_is_present(self.newMessageIcon, time=4) == True:
            self.telegramBot.send_message(-877986264, "!!! You Received a new message !!!")

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
        self.step.jsXpathClick(self.ContactOwnerButton)
        time.sleep(2)
        self.step.input_text(self.MessageInputField, text)
        self.step.click_on_element(self.SendMessageButton, scrollInToView=True)
        time.sleep(1)
        self.step.specified_element_is_present(self.SuccessMessageText, time=5)
        self.step.click_on_element(self.CloseMessageWindow, scrollInToView=True)
        time.sleep(1)
