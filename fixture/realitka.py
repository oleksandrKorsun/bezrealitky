import time

from helpers.csvHelper import CsvHelper
from helpers.telegramBotHelper import TelegramBotHelper


class RealitkaHelper:
    csvFile = CsvHelper("file_with_flats.csv")
    telegramBot = TelegramBotHelper()

    FIRST_CHECK_BOX = "(//span[@class='custom-control-indicator'])[3]"
    SECOND_CHECK_BOX = "(//span[@class='custom-control-indicator'])[4]"
    CHECK_BOX_BEFORE_SEND_LETTER = "(//span[@class='custom-control-indicator'])[9]"
    DALSI_INZERATY = '.p-lg-20 .btn.btn-secondary.btn-icon.btn-shadow.btn-sm'
    SEND_MESSAGE_TO_OWNER = "(//a[@class='send-message btn btn-success btn-icon btn-icon-lg js-send-message'])[2]"
    SEND_MESSAGE_BUTTON = '.send-message-submit.btn.btn-primary.btn-shadow'
    LOG_IN_BUTTON = '.btn.btn-primary.btn-lg'
    MY_ACCOUNT_ICON = '.m-profile__account'
    LOG_OUT_BUTTON = '.m-profile__sub__link--logout.nav-link.m-profile__sub__link'
    MESSAGE_TO_OWNER_TEXT_AREA = '#send-message > div > div > div.modal-body > div > textarea'
    VPORADKU_BUTTON = "//a[text()='V pořádku']"
    CLOSE_MODAL_AFTER_SEND_MESSAGE = "(//span[@aria-hidden='true' and text()='×'])[10]"
    POST_WAS_DELETED = "//h2[contains(text(), 'Inzerát byl odstraněn')]"
    FLAT_HEADER = "//h1[@class='heading__title mb-4 mb-md-1']"
    FLAT_DESCRIPTION = "//p[@class='b-desc__info']"
    ADD = "//div[@id='collapse_text']"
    maximum_price_of_flat = "17"
    reality_username = "bersh92@gmail.com"
    reality_password = "bersh06061989"

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
        time.sleep(2)
        self.step.specified_element_is_not_present(self.SuccessLogInMessage, 5)

    def find_flats(self):
        list_of_elements = len(self.step.get_list_of_elements(self.LIST_OF_FLATS))
        for element in range(list_of_elements):
            self.wd.execute_script(
                "arguments[0].scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'start' });", self.step.get_list_of_elements(self.LIST_OF_FLATS)[element])
            time.sleep(2)
            self.step.get_list_of_elements(self.LIST_OF_FLATS)[element].click()
            self.step.specified_element_is_not_present(self.LoadingSpinner, 5)
            if self.step.is_element_present(self.POST_WAS_DELETED, time=1) == True:
                self.click_on_dog_button_and_load_flats()
            elif float(self.step.get_element_text(self.PRICE_OF_THE_FLAT).split(' ')[0]) <= float(self.maximum_price_of_flat):
                if self.csvFile.check_if_element_in_csv(self.get_flat_description_id()) == False:
                    self.csvFile.write_to_csv(self.get_flat_description_id())
                    self.csvFile.write_to_csv('\n')
                    # self.send_message_to_owner('message')
                    self.telegramBot.send_message(248932976, str(self.wd.current_url))
                self.click_on_dog_button_and_load_flats()
            else:
                self.click_on_dog_button_and_load_flats()
            list_of_elements = list_of_elements - 1

    def click_on_dog_button_and_load_flats(self):
        self.step.click_on_element(self.DOG_BUTTON)
        self.load_all_flats_list()

    def load_all_flats_list(self):
        time.sleep(1)
        self.step.specified_element_is_not_present(self.LoadingSpinner, 5)
        time.sleep(1)
        if self.step.is_element_present(self.NacistDalsiButton, time=1) == True:
            while self.step.is_element_present(self.NacistDalsiButton, time=1) == True:
                self.step.click_on_element(self.NacistDalsiButton, scrollInToView=True)
                time.sleep(1)

    def get_flat_description_id(self):
        result = self.step.get_element_text(self.ID_NUMBER_OF_THE_FLAT)
        return result

    def hide_add(self):
        if self.step.is_element_present(self.ADD, time=1) == True:
            self.step.click_on_element(self.ADD)

    def check_flat_price(self):
        price = self.step.get_element_text(self.PRICE_OF_THE_FLAT)
        if "+" in price:
            price_new = price.split(' ')
            actual_price = float(price_new[0]) + float(price_new[3])
        else:
            price_new = price.split(' ')
            actual_price = float(price_new[0])
        return actual_price
