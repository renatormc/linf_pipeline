from blessed import Terminal

term = Terminal()

with term.location(0, 5):  # Move to row 5, column 10
    print("Hello at (10, 5)")

with term.location(20, 10):  # Move to row 10, column 20
    print("Another message at (20, 10)")