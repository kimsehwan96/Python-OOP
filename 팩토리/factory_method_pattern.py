from abc import ABCMeta, abstractmethod
from typing import List


class Section(metaclass=ABCMeta):
    @abstractmethod
    def describe(self):
        raise NotImplementedError


class PersonalSection(Section):
    def describe(self):
        print("Personal section")


class AlbumSection(Section):
    def describe(self):
        print("Album section")


class PatentSection(Section):
    def describe(self):
        print("Patent section")


class PublicationSection(Section):
    def describe(self):
        print("publication Section")


class Profile(metaclass=ABCMeta):
    def __init__(self) -> None:
        self.sections = []
        self.createProfile()

    @abstractmethod
    def createProfile(self) -> None:
        raise NotImplementedError

    def getSection(self) -> List[Section]:
        return self.sections

    def addSection(self, section: Section) -> None:
        self.sections.append(section)


class LinkedIn(Profile):
    def createProfile(self):
        self.addSection(PersonalSection())
        self.addSection(PatentSection())
        self.addSection(PublicationSection())


class FaceBook(Profile):
    def createProfile(self):
        self.addSection(PersonalSection())
        self.addSection(AlbumSection())


if __name__ == "__main__":
    profile_type = input("Which Profile you'd like to create? [LinkedIn or FaceBook]")
    profile = eval(profile_type)()
    print("Creating profile....", type(profile).__name__)
    print("Profile has sections --", profile.getSection())
