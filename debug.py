from runelite_library.bank import Bank
from runelite_library.window_management import RuneLiteWindow

rl = RuneLiteWindow()
rl.activate()

b = Bank(rl)
if b.return_to_bank():
    print("Done!")
else:
    print("Nope!")
