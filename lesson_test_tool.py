"""
Helps to pass the lesson in the bot according to the parameters set by the tester
"""


########################################################################################################################
import logging
import sys
import time
import random
import re
import sqlalchemy

from selenium import webdriver
import selenium.common.exceptions
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.wait import WebDriverWait
import config.config


########################################################################################################################
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    stream=sys.stdout,
    format='[%(asctime)s]:[%(levelname)s]:[%(filename)s]:[%(lineno)d]: %(message)s',
)


########################################################################################################################
browser = webdriver.Firefox(
    executable_path=r'geckodriver\geckodriver.exe',
)
browser.set_window_size(
    config.config.SIZE_X,
    config.config.SIZE_Y
)


########################################################################################################################
engine = sqlalchemy.create_engine(config.config.MY_SQL, pool_recycle=3600, echo=True)


########################################################################################################################
def auth():
    # open telegram
    try:
        time.sleep(2.5)
        phone_login = browser.find_element_by_css_selector(
            '#auth-pages > div > div.tabs-container.auth-pages__container > div.tabs-tab.page-signQR.active > div > div.input-wrapper > button:nth-child(1) > div'
        )
        logger.info('User have to auth')
        phone_login.click()
    except (
            selenium.common.exceptions.NoSuchElementException,
            selenium.common.exceptions.ElementNotInteractableException
    ) as e:
        logger.warning(f'Fail finding phone loging button {e}')

    # phone input
    try:
        time.sleep(4)
        number_input = browser.find_element_by_css_selector(
             'html.is-firefox.no-backdrop.no-touch.night body.animation-level-2.is-left-column-shown div#auth-pages.whole div.scrollable.scrollable-y.no-scrollbar div.tabs-container.auth-pages__container div.tabs-tab.page-sign.active div.container div.input-wrapper div.input-field.input-field-phone div.input-field-input'
        )
        number_input.clear()
        user_phone_value = input('>>> Please, send me number to authorization with country code: ')
        number_input.send_keys(user_phone_value)
        next_button = browser.find_element_by_css_selector(
            'html.is-firefox.no-backdrop.no-touch.night body.animation-level-2.is-left-column-shown div#auth-pages.whole div.scrollable.scrollable-y.no-scrollbar div.tabs-container.auth-pages__container div.tabs-tab.page-sign.active div.container div.input-wrapper button.btn-primary.btn-color-primary.rp div.c-ripple'
        )
        next_button.click()
    except (
            selenium.common.exceptions.NoSuchElementException,
            selenium.common.exceptions.ElementNotInteractableException
    ) as e:
        logger.warning(f'Fail send phone {e}')

    # code input
    try:
        time.sleep(1)
        code_input = browser.find_element_by_css_selector(
            'html.is-firefox.no-backdrop.no-touch.night body.animation-level-2.is-left-column-shown div#auth-pages.whole div.scrollable.scrollable-y.no-scrollbar div.tabs-container.auth-pages__container div.tabs-tab.page-authCode.active div.container.center-align div.input-wrapper div.input-field input.input-field-input'
        )
        code_input.clear()
        user_code_value = input('>>> Please, send me a code: ')
        code_input.send_keys(user_code_value)
    except (
            selenium.common.exceptions.NoSuchElementException,
            selenium.common.exceptions.ElementNotInteractableException
    ) as e:
        logger.warning(f'Fail send code {e}')

    # 2-f code input
    try:
        time.sleep(1)
        ath_code_input = browser.find_element_by_css_selector(
            'html.is-firefox.no-backdrop.no-touch.night body.animation-level-2.is-left-column-shown div#auth-pages.whole div.scrollable.scrollable-y.no-scrollbar div.tabs-container.auth-pages__container div.tabs-tab.page-password.active div.container.center-align div.input-wrapper div.input-field.input-field-password input.input-field-input'
        )
        ath_code_input.clear()
        user_ath_code_value = input('>>> Please, send me a 2-fa code: ')
        ath_code_input.send_keys(user_ath_code_value)
        next_button = browser.find_element_by_css_selector(
            'html.is-firefox.no-backdrop.no-touch.night body.animation-level-2.is-left-column-shown div#auth-pages.whole div.scrollable.scrollable-y.no-scrollbar div.tabs-container.auth-pages__container div.tabs-tab.page-password.active div.container.center-align div.input-wrapper button.btn-primary.btn-color-primary.rp div.c-ripple'
        )
        next_button.click()
    except (
            selenium.common.exceptions.NoSuchElementException,
            selenium.common.exceptions.ElementNotInteractableException
    ) as e:
        logger.warning(f'Fail send auth code {e}')


def lesson_start():

    user_start_flag = input('>>> Are you ready to start(Y/n): ')
    if user_start_flag != 'Y':
        lesson_start()

    # find the bot
    try:
        time.sleep(1)
        finding_tool = browser.find_element_by_css_selector(
            'html.is-firefox.no-backdrop.no-touch.night body.animation-level-2.is-left-column-shown div#page-chats.whole.page-chats div#main-columns.tabs-container div#column-left.tabs-tab.chatlist-container.sidebar.sidebar-left.main-column div.sidebar-slider.tabs-container div.tabs-tab.sidebar-slider-item.item-main.active div.sidebar-header div.input-search input.input-field-input.i18n.input-search-input'
        )
        finding_tool.clear()
        finding_tool.send_keys(config.config.BOT_LINK)
        time.sleep(2)
        bot_chat = browser.find_element_by_css_selector(
            'html.is-firefox.no-backdrop.no-touch.night body.animation-level-2.is-left-column-shown div#page-chats.whole.page-chats div#main-columns.tabs-container div#column-left.tabs-tab.chatlist-container.sidebar.sidebar-left.main-column div.sidebar-slider.tabs-container div.tabs-tab.sidebar-slider-item.item-main.active div.sidebar-content.transition.zoom-fade div#search-container.transition-item.sidebar-search.active div.scrollable.scrollable-y div.search-super div.search-super-tabs-container.tabs-container div.search-super-container-chats.tabs-tab.active div.search-super-content-chats div.search-group.search-group-contacts.is-short ul.chatlist a.chatlist-chat.rp div.c-ripple'
            )
        bot_chat.click()
    except (
            selenium.common.exceptions.NoSuchElementException,
            selenium.common.exceptions.ElementNotInteractableException
    ) as e:
        logger.warning(f'Fail find bot chat {e}')
        return

    # start lesson
    try:
        time.sleep(1)
        # # 'html.is-firefox.no-backdrop.no-touch.night body.animation-level-2.has-chat div#page-chats.whole.page-chats div#main-columns.tabs-container div#column-center.tabs-tab.main-column div.chats-container.tabs-container div.chat.tabs-tab.active.type-chat div.chat-input div.chat-input-container div.rows-wrapper-wrapper div.rows-wrapper.chat-input-wrapper div.new-message-wrapper.has-offset div.input-message-container div.input-message-input.i18n.scrollable.scrollable-y.no-scrollbar'
        terminal = browser.find_element_by_css_selector(
            'html.is-firefox.no-backdrop.no-touch.night body.animation-level-2.has-chat div#page-chats.whole.page-chats div#main-columns.tabs-container div#column-center.tabs-tab.main-column div.chats-container.tabs-container div.chat.tabs-tab.active.type-chat div.chat-input div.chat-input-container div.rows-wrapper-wrapper div.rows-wrapper.chat-input-wrapper div.new-message-wrapper div.input-message-container div.input-message-input.i18n.scrollable.scrollable-y.no-scrollbar'
        )
        terminal.clear()
        terminal.send_keys('/cancel')
        terminal.send_keys(Keys.ENTER)
        time.sleep(1)
        terminal.send_keys('/lesson')
        terminal.send_keys(Keys.ENTER)

        time.sleep(3)
        start_button = browser.find_element_by_css_selector(
            'html.is-firefox.no-backdrop.no-touch.night body.animation-level-2.has-chat div#page-chats.whole.page-chats div#main-columns.tabs-container div#column-center.tabs-tab.main-column div.chats-container.tabs-container div.chat.tabs-tab.active.type-chat div.bubbles.has-groups.has-sticky-dates.scrolled-down div.scrollable.scrollable-y div.bubbles-inner.has-rights section.bubbles-date-group div.bubbles-group div.bubble.with-reply-markup.hide-name.is-in.is-group-last div.bubble-content-wrapper div.reply-markup div.reply-markup-row button.reply-markup-button.rp.tgico div.c-ripple'
        )
        start_button.click()
    except (
            selenium.common.exceptions.NoSuchElementException,
            selenium.common.exceptions.ElementNotInteractableException
    ) as e:
        logger.warning(f'Fail start lesson {e}')
        return


def lesson_execute():

    terminal = browser.find_element_by_css_selector(
        'html.is-firefox.no-backdrop.no-touch.night body.animation-level-2.has-chat div#page-chats.whole.page-chats div#main-columns.tabs-container div#column-center.tabs-tab.main-column div.chats-container.tabs-container div.chat.tabs-tab.active.type-chat div.chat-input div.chat-input-container div.rows-wrapper-wrapper div.rows-wrapper.chat-input-wrapper div.new-message-wrapper div.input-message-container div.input-message-input.i18n.scrollable.scrollable-y.no-scrollbar'
    )

    for height in range(15):

        try:
            page_down_buttons = browser.find_element_by_css_selector(
                'html.is-firefox.no-backdrop.no-touch.night body.animation-level-2.has-chat div#page-chats.whole.page-chats div#main-columns.tabs-container div#column-center.tabs-tab.main-column div.chats-container.tabs-container div.chat.tabs-tab.active.type-chat div.chat-input div.chat-input-container button.btn-circle.btn-corner.z-depth-1.bubbles-corner-button.bubbles-go-down.tgico-arrow_down.rp'
            )
            page_down_buttons.click()
        except Exception as e:
            pass

        time.sleep(5)
        bot_test_text = browser.find_elements_by_css_selector(
            'html.is-firefox.no-backdrop.no-touch.night body.animation-level-2.has-chat div#page-chats.whole.page-chats div#main-columns.tabs-container div#column-center.tabs-tab.main-column div.chats-container.tabs-container div.chat.tabs-tab.active.type-chat div.bubbles.has-groups.has-sticky-dates.scrolled-down div.scrollable.scrollable-y div.bubbles-inner.has-rights section.bubbles-date-group div.bubbles-group div.bubble.hide-name.is-in.can-have-tail.is-group-last div.bubble-content-wrapper div.bubble-content div.message.spoilers-container'
        )[-1].text

        logger.info(f'[{height}]: \n\n{bot_test_text}\n')

        current = {'chose': (), 'a': '', 'b': '', 'c': '', 'd': ''}
        question = re.compile('"(.*)"', re.DOTALL).findall(bot_test_text)[0]
        if 'Select the correct word by description' in bot_test_text:
            current['chose'] = ('word', question)
        else:
            current['chose'] = ('description', question)

        logger.info(f'[{height}]: {current}')

        answers = ('a', 'b', 'c', 'd')
        if current['chose'][0] == 'word':
            for i in range(4):
                current[answers[i]] = re.compile(
                    rf'((\s{answers[i]}\.\s)(.*)(\n))'
                ).findall(bot_test_text)[0][2].strip()
            query_answer = list(engine.execute(
                'SELECT * FROM words '
                'WHERE description = "{}" '.format(current['chose'][1])
            ))[0][1]
        else:
            for i in range(4):
                if i == 3:
                    last_group = r'\d\d:\d\d'
                else:
                    last_group = fr'{answers[i + 1]}\.\s'
                current[answers[i]] = re.compile(
                    rf'((\s{answers[i]}\.\s)(.*)({last_group}))', re.DOTALL
                ).findall(bot_test_text)[0][2].strip()
            query_answer = list(engine.execute(
                'SELECT * FROM words '
                'WHERE word = "{}" '.format(current['chose'][1])
            ))[0][2]

        logger.info(f'[{height}]: \n {current} \n {query_answer}')

        right_answer = None
        for k, v in current.items():
            if v == query_answer:
                right_answer = k

        logger.info(f'[{height}]: Right answer {right_answer}')

        if not right_answer:
            for i in answers:
                terminal.clear()
                terminal.send_keys(i)
                terminal.send_keys(Keys.ENTER)
                time.sleep(3)
                next_button = browser.find_elements_by_css_selector(
                    'html.is-firefox.no-backdrop.no-touch.night body.animation-level-2.has-chat div#page-chats.whole.page-chats div#main-columns.tabs-container div#column-center.tabs-tab.main-column div.chats-container.tabs-container div.chat.tabs-tab.active.type-chat div.bubbles.scrolled-down.has-groups.has-sticky-dates div.scrollable.scrollable-y div.bubbles-inner.has-rights section.bubbles-date-group div.bubbles-group div.bubble.with-reply-markup.hide-name.is-in.is-group-first.is-group-last div.bubble-content-wrapper div.reply-markup div.reply-markup-row button.reply-markup-button.rp.tgico'
                )[-2]
                next_button.click()
                if 'Next' in next_button.text:
                    break

        terminal.clear()
        terminal.send_keys(right_answer)
        terminal.send_keys(Keys.ENTER)

        time.sleep(3)

        next_button = browser.find_elements_by_css_selector(
            'html.is-firefox.no-backdrop.no-touch.night body.animation-level-2.has-chat div#page-chats.whole.page-chats div#main-columns.tabs-container div#column-center.tabs-tab.main-column div.chats-container.tabs-container div.chat.tabs-tab.active.type-chat div.bubbles.scrolled-down.has-groups.has-sticky-dates div.scrollable.scrollable-y div.bubbles-inner.has-rights section.bubbles-date-group div.bubbles-group div.bubble.with-reply-markup.hide-name.is-in.is-group-first.is-group-last div.bubble-content-wrapper div.reply-markup div.reply-markup-row button.reply-markup-button.rp.tgico'
        )[-2]
        next_button.click()

########################################################################################################################
def main():
    logger.info('Test tool start')
    browser.get('https://web.telegram.org/k/')

    logger.info('Telegram auth start')
    auth()

    logger.info('Telegram lesson start')
    lesson_start()

    logger.info('Telegram lesson execution')
    lesson_execute()

    logger.info('Done.')


########################################################################################################################
if __name__ == '__main__':
    main()
