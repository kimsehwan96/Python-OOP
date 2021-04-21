from subsystems import (
    Hotelier,
    Florist,
    Musician,
    Caterer
)


class EventManager:

    def __init__(self):
        self.musician = Musician()
        self.caterer = Caterer()
        self.florist = Florist()
        self.hotelier = Hotelier()
        print('Event manager called (instance)')

    def arrange(self):
        self.hotelier.book_hotel()

        self.florist.set_flower_requirements()

        self.caterer.set_cuisine()

        self.musician.set_music_type()
