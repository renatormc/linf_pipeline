from blessed import Terminal
import time



def draw_screen(term: Terminal, objects: int, cases: int, progress: float) -> None:
    with term.location(0, 0):  
        print(term.clear) 
        print(term.bold("Console UI Example"))
        print("".ljust(30, "-"))
        print(f"{term.bold('Number of objects:')} {objects}")
        print(f"{term.bold('Number of cases:')} {cases}")
        
        # Draw progress bar
        bar_length = 40 
        completed = int(bar_length * progress)
        bar = "█" * completed + "-" * (bar_length - completed)
        print(f"{term.bold('Progress:')} [{bar}] {int(progress * 100)}%")

def main():
    term = Terminal()
    objects = 10
    cases = 5
    progress = 0.0
    
    with term.fullscreen(), term.hidden_cursor():  # Fullscreen mode & hide cursor
        for i in range(11):
            draw_screen(term, objects, cases, progress)
            time.sleep(0.5)  # Simulate progress update
            progress += 0.1
    
    print(term.move_down(2) + "Process complete!")

if __name__ == "__main__":
    main()
