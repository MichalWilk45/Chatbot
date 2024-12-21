# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"
import json
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet


class ActionShowMenu(Action):
    def name(self) -> Text:
        return "action_show_menu"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print('ActionShowMenu')
        
        try:
            with open('menu.json', 'r') as f:
                data = json.load(f)
                menu = data["items"]
                print(menu)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return []
        except FileNotFoundError:
            print("menu.json file not found.")
            return []


        menu_text = (
            f"Items: {[item['name'] for item in menu]}\n"
            f"Prices: {[item['price'] for item in menu]}"
        )

        print([item['name'] for item in menu])
        
        dispatcher.utter_message(text=f"Here's our menu:\n{menu_text}")
        #dispatcher.utter_message(text="Here's our menu:")
        return []

class ActionShowOpeningHours(Action):
    def name(self) -> Text:
        return "action_show_opening_hours"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        print('ActionShowMenu')
        
        try:
            with open('opening_hours.json', 'r') as f:
                data = json.load(f)
                hours = data["items"]
               # print(hours)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return []
        except FileNotFoundError:
            print("opening_hours.json file not found.")
            return []


        hours_text = (
                f"Days: {', '.join([day for day in hours])}\n"
                f"Opening: {', '.join([str(times['open']) for times in hours.values()])}\n"
                f"Closing: {', '.join([str(times['close']) for times in hours.values()])}"
        )

        #print([item['name'] for item in menu])
        
        dispatcher.utter_message(text=f"Here's our hours:\n{hours_text}")
        #dispatcher.utter_message(text="Here's our menu:")
        return []
    

class ActionAddAndSaveOrder(Action):
    def name(self) -> str:
        return "action_add_and_save_order"

    def run(self, dispatcher, tracker, domain):
        # Get the current items in the menu_items slot
        current_items = tracker.get_slot("menu_items") or []

        # Extract new items from user input (via entities)
        new_items = list(tracker.get_latest_entity_values("menu_item"))

        try:
            with open('menu.json', 'r') as f:
                data = json.load(f)
                menu = data["items"]
                print('Menu loaded')
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return []
        except FileNotFoundError:
            print("menu.json file not found.")
            return []
        
        print(f"New Items {new_items}")
        print(f"Menu: {menu}")

        menu_names = [item['name'] for item in menu]

        valid_items = [item for item in new_items if item in menu_names]
        if not valid_items:
            dispatcher.utter_message(text="The items you mentioned are not on the menu.")
            return []

        # Update the order with new items
        updated_items = current_items + valid_items

        # Save the updated order to a JSON file
        order_data = {"order": updated_items}


        try:
            with open("order.json", "w") as order_file:
                json.dump(order_data, order_file)
            dispatcher.utter_message(text=f"I've added {', '.join(valid_items)} to your order and saved it.")
        except IOError as e:
            dispatcher.utter_message(text="There was an error saving your order. Please try again.")
            return []

        # Update the slot with the new order
        return [SlotSet("menu_items", updated_items)]


