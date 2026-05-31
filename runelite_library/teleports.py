from runelite_library.interact import RuneliteComponent, open_interface
from runelite_library.window_management import RuneLiteWindow
from too_many_items import (
    ChatMenuObjects,
    MenuObjects,
    NormalSpellObjects,
    WearableObjects,
)


class Spells(RuneliteComponent):
    @staticmethod
    def open_spellbook(original_function):
        def wrapper(*args, **kwargs):
            open_interface("spells")
            result = original_function(*args, **kwargs)
            open_interface("inventory")
            return result

        return wrapper

    @open_spellbook
    def normal_spellbook(self, spell: str):
        """
        Uses a spell from the normal spellbook. Finishes by opening inventory.

        Args:
            spell (str): matches user input to NormalSpellObjects in `too_many_items`

        Raises:
            KeyError: when you input an entry that doesn't exist

        """
        try:
            return self.client.click(getattr(NormalSpellObjects, spell))
        except AttributeError:
            raise KeyError(f"Spell {spell} does not exist in NormalSpellObjects")


class Wearable(RuneliteComponent):
    def __init__(self, rl: RuneLiteWindow, equipped: bool = False):
        super().__init__(rl)  # initialize RuneliteComponent
        self.equipped = equipped

    @staticmethod
    def require_equipment_interface(func):
        """Opens equipment interface before executing"""

        def wrapper(self, *args, **kwargs):
            if getattr(self, "equipped", False):
                open_interface("equipment")
            result = func(self, *args, **kwargs)
            open_interface("inventory")
            return result

        return wrapper

    @require_equipment_interface
    def teleport(self, item: str, location: str):
        """
        Uses an item to teleport to a location. Finishes by opening inventory.

        Args:
            item (str): matches the item to WearableObjects in `too_many_items`
            location (str): matches entry in either MenuObjects or ChatMenuObjects depending on if the item is equipped.

        Raises:
            KeyError: when you input an entry that doesn't exist

        """
        try:
            wearable_object = getattr(WearableObjects, item)
        except AttributeError:
            raise KeyError(f"Item '{item}' does not exist in WearableObjects.")

        try:
            if self.equipped:
                menu_object = getattr(MenuObjects, location)
            else:
                menu_object = getattr(ChatMenuObjects, location)
        except AttributeError:
            raise KeyError(f"Location '{location}' does not exist in MenuObjects.")

        self.inventory.click(
            rs_object=wearable_object,
            click_type="right",
        )

        if not self.equipped:
            self.client.click(MenuObjects.rub)  # This only applies to jewelry
        self.client.click(menu_object)
