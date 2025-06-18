import time
from playwright.sync_api import sync_playwright

JOLT_LOGIN_URL = "https://app.joltup.com/account#/login"
JOLT_LISTS_URL = "https://app.joltup.com/content/lists/"

JOLT_GROUP_NAME = "Group_001"
DRIVER_CHECKLISTS_FOLDER_NAME = "Driver Checklists"
SCRIPT_TESTS_FOLDER_NAME = "Script Tests"

URP_MENU_4_FILEPATH = "URP_4.txt"

DAYS_OF_WEEK = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
MEAL_TIMES = ["Breakfast", "Lunch", "Dinner"]
ACCOUNT_NAMES = ["URP_North", "URP_South", "Aria_WPB", "Aria_Boca", "Arcstone", "Mandala", "Legacy", "Ignite", "Archway"]

def main():
    with open(URP_MENU_4_FILEPATH, 'r') as menu:
        content = menu.read()
    
    lines = content.split('\n')
    account_name = lines[0]
    menu_number = int(lines[1][-1])
    
    username, password = input("username and password separated by space: ").split(" ")
    
    playwright, browser, page = start_playwright()
    jolt_login(page, username, password)
    go_to_lists_homepage(page)
    set_content_group_mode(page)
    set_group_root_folder(page, JOLT_GROUP_NAME)
    click_on_text(page, DRIVER_CHECKLISTS_FOLDER_NAME)
    click_on_text(page, SCRIPT_TESTS_FOLDER_NAME)
    click_add_list(page, "test name")
    click_add_list_item(page)
    click_checkmark_item(page)
    fill_prompt_text(page, "checkmark test fill")
    click_add_list_item(page)
    click_photo_item(page)
    fill_prompt_text(page, "photo test fill")
    save_list(page)
    exit_list(page)
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
    
def jolt_login(page, username, password):
    page.goto(JOLT_LOGIN_URL)
    page.get_by_role("textbox", name="email").fill(username)
    page.get_by_role("textbox", name="password").fill(password)
    page.get_by_role("button", name="Submit login").click()
    page.get_by_role("heading", name="Lists Overview").wait_for(state="visible")
    
def go_to_lists_homepage(page):
    page.goto(JOLT_LISTS_URL)
    page.get_by_role("table").wait_for(state="visible")

def set_content_group_mode(page):
    page.locator(".entity-button.isEntitySwitcherButton").click()
    page.locator(".entity-tiles").wait_for(state="visible")
    page.locator(".is-content-group").click()
    page.locator(".list-template-header").wait_for(state="hidden")
    page.locator(".list-template-header").wait_for(state="visible")

def set_group_root_folder(page, folder_name):
    page.locator(".name.body2").get_by_text(folder_name).click()
    
def click_on_text(page, text):
    page.get_by_text(text).click()
    
def click_add_list(page, list_name):
    page.get_by_test_id("button-circle").click()
    page.locator("#input-list-title").fill(list_name)
    page.get_by_role("button").get_by_text("Confirm").click()
    page.get_by_role("heading", name="Edit List Name").wait_for(state="hidden")
    
def click_add_list_item(page):
    page.get_by_role("button").get_by_text("+ ADD ITEM").click()
    page.get_by_role("heading", name="Select an item type").wait_for(state="visible")
    
def click_checkmark_item(page):
    page.locator(".list-check-bold").first.click()
    page.locator(".list-check-bold").first.wait_for(state="hidden")
    
def click_photo_item(page):
    page.locator(".list-camera").first.click()
    page.locator(".list-camera").first.wait_for(state="hidden")
        
def fill_prompt_text(page, text):
    page.wait_for_timeout(500)
    page.locator(".textarea#textarea-text").fill(text)
    page.wait_for_timeout(500)
    
def save_list(page):
    page.get_by_role("button").get_by_text("SAVE").click()

def exit_list(page):
    page.locator(".list-arrow-left").click()
    page.get_by_role("table").wait_for(state="visible")

if __name__ == "__main__":
    main()