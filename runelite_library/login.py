from runelite_library.interact import (
    RuneliteComponent,
    move_to_and_click,
    open_interface,
    set_screen,
)
from too_many_items import LoginObjects, PlayerObjects


class LoginLogout(RuneliteComponent):
    def logout_now(self):
        open_interface("logout")
        move_to_and_click(self.logout.random_coordinate_in_area())

    def _handle_alternatives(self) -> tuple:
        alts = [LoginObjects.try_again, LoginObjects.ok]

        for image in alts:
            coords = self.client.find_by_image(image)
            if not coords:
                continue

            move_to_and_click(coords)

    def login_now(self):
        if self.client.find_player():
            return True

        self._handle_alternatives()

        self.client.click(LoginObjects.play_now_button)
        self.client.click(LoginObjects.click_to_play_button)
        if not self.client.wait_for_element(PlayerObjects.player_tile, 20):
            return False

        set_screen(self.rl)
        return True
