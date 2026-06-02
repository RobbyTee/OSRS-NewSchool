from runelite_library.interact import RuneliteComponent
from too_many_items import BankObjects, MiscObjects, ToolTips


class Bank(RuneliteComponent):
    def open_bank(self):
        self.client.click(
            rs_object=BankObjects.bank,
            mouse_tooltip=ToolTips.bank,
        )
        return self.play_window.wait_for_element(BankObjects.deposit_inventory)

    def deposit_inventory(self):
        return self.play_window.click(BankObjects.deposit_inventory)

    def deposit_equipment(self):
        return self.play_window.click(BankObjects.deposit_equipment)

    def open_tab(self, tab: str):
        return self.play_window.click(tab)

    def withdraw(
        self,
        rs_objects: list[str],
        quantity: int | str = 1,
        check_quantity: bool = False,
    ):
        """
        With the bank and correct tab open, withdraws items from that tab in the specified quantity.

        Might have it withdraw "x" in the future. Use the special function `withdraw_14()` as needed.

        Args:
            rs_objects (list[str]): The item to withdraw.
            quantity (int | str): The amount to withdraw. Defaults to 1, but can be one of:
                - 1
                - 5
                - 10
                - "all"
            check_quantity (bool): Verifies the quantity of item is acceptable for task

        Raises:
            KeyError: if quantity does not match a valid option.

        """
        quantity_dict = {
            1: BankObjects.quantity_1,
            5: BankObjects.quantity_5,
            10: BankObjects.quantity_10,
            "all": BankObjects.quantity_all,
        }

        if quantity in quantity_dict:
            self.play_window.click(quantity_dict.get(quantity))
        else:
            raise KeyError

        mouse_tooltip = MiscObjects.good if check_quantity else None

        for item_to_withdraw in rs_objects:
            self.play_window.click(
                item_to_withdraw,
                mouse_tooltip=mouse_tooltip,
            )

    def withdraw_14(self, rs_objects: tuple):
        """
        Right clicks rs_object and presses "Withdraw 14". Must have preset Withdraw X to 14!

        Args:
            rs_objects (tuple): A list containing exactly two items.

        Raises:
            ValueError: If rs_objects does not contain exactly 2 items.
            ValueError: When "Withdraw 14" isn't found.

        """
        if len(rs_objects) != 2:
            raise ValueError(
                f"withdraw_14 expected exactly 2 objects, got {len(rs_objects)}",
            )

        for item in rs_objects:
            self.play_window.click(item, click_type="right")
            if not self.play_window.click(BankObjects.withdraw_14):
                raise ValueError("Withdraw 14 not found as a menu option")

    def return_to_bank(self):
        pass
