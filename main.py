import time
from playwright.sync_api import sync_playwright, expect

JOLT_LOGIN_URL = "https://app.joltup.com/account#/login"
JOLT_LISTS_URL = "https://app.joltup.com/content/lists/"

JOLT_GROUP_NAME = "Group_001"
DRIVER_CHECKLISTS_FOLDER_NAME = "Driver Checklists"

URP_MENU_4_FILEPATH = "URP_4.txt"

DAYS_OF_WEEK = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
MEAL_TIMES = ["Breakfast", "Lunch", "Dinner"]

def main():
    with open(URP_MENU_4_FILEPATH, 'r') as menu:
        content = menu.read()
    
    lines = content.split('\n')
    account_name = lines[0]
    menu_number = int(lines[1][-1])
    
    playwright, browser, page = start_playwright()
    username, password = input("username and password separated by space: ").split(" ")
    login(page, username, password)
    go_to_lists_homepage(page)
    set_group_mode(page)
    set_group_root_folder(page)
    select_folder(page, DRIVER_CHECKLISTS_FOLDER_NAME)
    
    add_list(page, "test name")
    
    add_list_item(page)
    page.wait_for_timeout(250)
    select_checkmark(page)
    page.wait_for_timeout(250)
    select_list_item(page, 0)
    page.wait_for_timeout(250)
    fill_prompt_text(page, "checkmark test fill")
    page.wait_for_timeout(250)
    
    add_list_item(page)
    page.wait_for_timeout(250)
    select_photo(page)
    page.wait_for_timeout(250)
    select_list_item(page, 1)
    page.wait_for_timeout(250)
    fill_prompt_text(page, "photo test fill")
    page.wait_for_timeout(250)
    
    save_list(page)
    
    time.sleep(10000)
    stop_playwright(browser, playwright)
    
def start_playwright():
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=False)
    page = browser.new_page()
    return playwright, browser, page
    
def stop_playwright(browser, playwright):
    browser.close()
    playwright.stop()
    
def login(page, username, password):
    page.goto(JOLT_LOGIN_URL)
    page.get_by_role("textbox", name="email").fill(username)
    page.get_by_role("textbox", name="password").fill(password)
    page.get_by_role("button", name="Submit login").click()
    expect(page.get_by_role("heading", name="Lists Overview")).to_be_visible()
    
def go_to_lists_homepage(page):
    page.goto(JOLT_LISTS_URL)

def set_group_mode(page):
    page.locator('//*[@id="header"]/div[1]/div[2]/button').click() # top right dropdown menu
    page.wait_for_timeout(1000)
    page.locator('//*[@id="php-menu-export"]/div/div/div/div/div[1]/div/div[2]/div/button[1]').click() # menu item
    page.wait_for_timeout(1000)

def set_group_root_folder(page):
    page.locator('//*[@id="root"]/div[1]/div/div[1]/div[1]/div[2]').click() # group root folder
    
def select_folder(page, name):
    page.get_by_text(DRIVER_CHECKLISTS_FOLDER_NAME).click()
    
def add_list(page, name):
    page.get_by_test_id("button-circle").click()
    page.get_by_test_id("input-list-titlefield-input-undefined").fill(name)
    page.get_by_role("button").get_by_text("Confirm").click()
    
def add_list_item(page):
    page.get_by_test_id("button-layout-addItem").click()
    
def select_checkmark(page):
    page.get_by_test_id("undefined").get_by_text("Checkmark").first.click()
    
def select_photo(page):
    page.get_by_test_id("undefined").get_by_text("Photo").first.click()
    
def select_list_item(page, item_index):
    page.locator("#itemTemplate-newItem-" + str(item_index + 1)).click()

def fill_prompt_text(page, text):
    page.get_by_test_id("textArea-field-textarea-undefined").fill(text)
    
def save_list(page):
    page.get_by_test_id("button-header-save").click()
    
if __name__ == "__main__":
    main()