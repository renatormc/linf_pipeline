from datetime import datetime
from blessed import Terminal
from sqlalchemy.orm import Session
from models import DBSession, Equipment
from repo import count_objects_in_equipments


class CustomTerminal(Terminal):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        with DBSession() as db_session:
            self.equipments = db_session.query(Equipment).all()
            

    def draw_screen(self, time: datetime | None, objects: int, cases: int, progress: float | None, db_session: Session) -> None:
        with self.location(0, 0):
            print(self.clear)
            print(self.bold("Pipeline simulator"))
            
            print("".ljust(30, "-"))
            for eq in self.equipments:
                n = count_objects_in_equipments(db_session, eq.name)
                print(f"{self.bold(eq.name)} ({eq.capacity}/{eq.lenght}): {n}")
                
            print("".ljust(30, "-"))
            if time:
                print(f"{self.bold('Time:')} {time.strftime("%d/%m/%Y %H:%M:%S")}")
            print(f"{self.bold('Finished objects:')} {objects}")
            print(f"{self.bold('Finished cases:')} {cases}")

            if progress is not None:
                # Draw progress bar
                bar_length = 40
                completed = int(bar_length * progress)
                bar = "█" * completed + "-" * (bar_length - completed)
                print(f"{self.bold('Progress:')} [{bar}] {progress * 100:.2f}%")