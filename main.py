import time
from playwright.sync_api import sync_playwright, expect

JOLT_LOGIN_URL = "https://app.joltup.com/account#/login"
JOLT_LISTS_URL = "https://app.joltup.com/content/lists/"

JOLT_GROUP_NAME = "Group_001"
DRIVER_CHECKLISTS_FOLDER_NAME = "Driver Checklists"

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
    set_group_mode(page, JOLT_GROUP_NAME)
    set_group_root_folder(page, JOLT_GROUP_NAME)
    click_on_text(page, DRIVER_CHECKLISTS_FOLDER_NAME)
    click_add_list(page, "test name")
    click_add_list_item(page)
    click_checkmark_item(page)
    fill_prompt_text(page, "checkmark test fill")
    click_add_list_item(page)
    click_photo_item(page)
    fill_prompt_text(page, "photo test fill")
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
    
def jolt_login(page, username, password):
    page.goto(JOLT_LOGIN_URL)
    page.get_by_role("textbox", name="email").fill(username)
    page.get_by_role("textbox", name="password").fill(password)
    page.get_by_role("button", name="Submit login").click()
    page.get_by_role("heading", name="Lists Overview").wait_for(state="visible")
    
def go_to_lists_homepage(page):
    page.goto(JOLT_LISTS_URL)
    page.get_by_role("table").locator(".list-template-index-table").wait_for(state="visible")
    # must use user facing elements table didnt work but "Name" in the column did since we can 
    # directly see it, try in all places to get to the front most part of the tree

def set_group_mode(page, group_name):
    page.locator(".entity-button isEntitySwitcherButton").click()
    page.locator(".entity-tiles").wait_for(state="visible")
    page.get_by_role("button").get_by_text(group_name).click()
    page.locator(".list-template-header").wait_for(state="hidden")
    page.locator(".list-template-header").wait_for(state="visible")

def set_group_root_folder(page, folder_name):
    page.locator(".name body2").get_by_text(folder_name).click()
    
def click_on_text(page, text):
    page.get_by_text(text).click()
    
def click_add_list(page, list_name):
    page.get_by_test_id("button-circle").click()
    page.get_by_role("textbox", name="list-title").fill(list_name)
    page.get_by_role("button").get_by_text("Confirm").click()
    page.get_by_role("heading", name="Edit List Name").wait_for(state="hidden")
    
def click_add_list_item(page):
    page.get_by_role("button").get_by_text("+ ADD ITEM").click()
    page.get_by_role("header", name="Select an item type").wait_for(state="visible")
    
def click_checkmark_item(page):
    page.locator(".list-check-bold").click()
    page.locator(".list-check-bold").wait_for(state="hidden")
    verify_list_item_active(page)
    
def click_photo_item(page):
    page.locator(".list-camera").click()
    page.locator(".list-camera").wait_for(state="hidden")
    verify_list_item_active(page)
    
def verify_list_item_active(page):
    item_index = page.locator(".itemTemplateCardDragDrop").count() - 1
    page.locator(".itemTemplateCardDragDrop").nth(item_index).locator("is-selected").wait_for(state="visible")
    
def fill_prompt_text(page, text):
    page.get_by_role("textbox", name="text").fill(text)
    
def save_list(page):
    page.get_by_role("button").get_by_text("SAVE").click()
    page.get_by_role("heading", name="Edit List Name").wait_for(state="visible")
    page.get_by_role("button").get_by_text("Cancel").click()
    page.get_by_role("heading", name="Edit List Name").wait_for(state="hidden")
    page.get_by_role("button", name="Previous Page Button").click()
    page.get_by_role("table").locator(".list-template-index-table").wait_for(state="visible")

if __name__ == "__main__":
    main()