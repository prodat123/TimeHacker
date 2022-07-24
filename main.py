from datetime import datetime, date, timedelta, time
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from playsound import playsound
import winsound
import keyboard

class DueDateWindow(Screen):
    homeworkDueDate = ObjectProperty(None)

    def press(self):
        homeworkDueDate = self.homeworkDueDate.text

        homeworkDueDateArray = homeworkDueDate.split("/")

        DueDateWindow.homeworkDueDate = date(int(homeworkDueDateArray[0]), int(homeworkDueDateArray[1]),
                                             int(homeworkDueDateArray[2]))

    pass


class TypeOfHomeworkWindow(Screen):
    homeworkType = ""

    def submit(self):
        TypeOfHomeworkWindow.homeworkType = self.homeworkType.text

        if TypeOfHomeworkWindow.homeworkType not in homeworkTypeOptions:
            self.errorLabel = Label(text="Please choose something that is within the options.")
            self.ids.typeOfHomeworkLayout.add_widget(self.errorLabel)
        else:
            if TypeOfHomeworkWindow.homeworkType == "essay":
                self.manager.current = "EssayHomeworkWindow"

            elif TypeOfHomeworkWindow.homeworkType == "open ended":
                self.manager.current = "OpenEndedHomeworkWindow"

    pass


class EssayHomeworkWindow(Screen):
    steps = []
    essayType = ""

    def submit(self):
        # determine how long the essay is
        essayLength = int(self.numOfWords.text)
        # determine if the essay is research or a fictional essay
        EssayHomeworkWindow.essayType = self.typeOfText.text
        # if it is a research essay then setup a different schedule than if it was a fictional essay
        if EssayHomeworkWindow.essayType == "research":
            EssayHomeworkWindow.steps = ["Do the research", "Write the thesis", "Create the outline", "Write the body",
                                         "Check and edit the content", "Check and edit grammar"]
        elif EssayHomeworkWindow.essayType == "fictional":
            EssayHomeworkWindow.steps = ["Create a setting",
                                         "Determine the conflict and climax", "Find a resolution", "Write the body", "Grammar check",
                                         "Revise"]

        print(EssayHomeworkWindow.steps)
        self.manager.current = "ScheduleWindow"

    pass


class OpenEndedHomeworkWindow(Screen):
    steps = []
    def submit(self):
        # how many questions are there
        numberOfQuestions = int(self.numOfQuestions.text)

        if numberOfQuestions < 12:
            playsound("Audio1.mp3")
        else:
            if numberOfQuestions >= 12:

                numberDivider = 3
                OpenEndedHomeworkWindow.steps = [f"Finish the first {round(numberOfQuestions/numberDivider)} questions", f"Finish the next {round(numberOfQuestions/numberDivider)} questions", f"Finish the next next {round(numberOfQuestions/numberDivider)} questions", "Finish the last questions"]



            self.manager.current = "ScheduleWindow"

    pass


class ScheduleWindow(Screen):
    daysLeftArray = []
    taskSchedule = []


    def timeSchedule(self, startDate, endDate, startTime):

        daysLeft = endDate - startDate
        for i in range(daysLeft.days + 1):
            day = startDate + timedelta(days=i)
            ScheduleWindow.daysLeftArray.append(day)

        # for i in range(len(daysLeftArray)):
        #     weekday = daysLeftArray[i].strftime("%A")
        #     print(weekday)

        if TypeOfHomeworkWindow.homeworkType == "essay":
            timeToAddFirst = 2
            startFirstTask = startTime + timedelta(hours=timeToAddFirst)


            timeToAddSecond = 4
            startSecondTask = startTime + timedelta(hours=timeToAddSecond)


            timeToAddThird = 6
            startThirdTask = startTime + timedelta(hours=timeToAddThird)

            timeToAddFourth = 7
            startFourthTask = startTime + timedelta(hours=timeToAddFourth)


            timeToAddFifth = 13
            startFifthTask = startTime + timedelta(hours=timeToAddFifth)

            timeToAddSixth = 15
            startSixthTask = startTime + timedelta(hours=timeToAddSixth)

            ScheduleWindow.taskSchedule.append(startFirstTask)
            ScheduleWindow.taskSchedule.append(startSecondTask)
            ScheduleWindow.taskSchedule.append(startThirdTask)
            ScheduleWindow.taskSchedule.append(startFourthTask)
            ScheduleWindow.taskSchedule.append(startFifthTask)
            ScheduleWindow.taskSchedule.append(startSixthTask)

            return startFirstTask, startSecondTask, startThirdTask, startFourthTask, startFifthTask, startSixthTask
        elif TypeOfHomeworkWindow.homeworkType == "open ended":

            timeToAddFirst = 1
            startFirstTask = startTime + timedelta(hours=timeToAddFirst)



            timeToAddSecond = 2
            startSecondTask = startTime + timedelta(hours=timeToAddSecond)



            timeToAddThird = 3
            startThirdTask = startTime + timedelta(hours=timeToAddThird)




            timeToAddFourth = 4
            startFourthTask = startTime + timedelta(hours=timeToAddFourth)



            ScheduleWindow.taskSchedule.append(startFirstTask)
            ScheduleWindow.taskSchedule.append(startSecondTask)
            ScheduleWindow.taskSchedule.append(startThirdTask)
            ScheduleWindow.taskSchedule.append(startFourthTask)
            return startFirstTask, startSecondTask, startThirdTask, startFourthTask


    def checkbox_click(self, instance, isActive, steps):





        pass

    def generateSchedule(self):

        currentDay = int(datetime.now().strftime("%d"))
        currentMonth = int(datetime.now().strftime("%m"))
        currentYear = int(datetime.now().strftime("%Y"))
        currentDate = date(currentYear, currentMonth, currentDay)

        currentTime = datetime.now()

        if len(EssayHomeworkWindow.steps) > 0:
            firstTask, secondTask, thirdTask, fourthTask, fifthTask, sixthTask = ScheduleWindow.timeSchedule(self,
                                                                                                             currentDate,
                                                                                                             DueDateWindow.homeworkDueDate,
                                                                                                             currentTime)


            self.ids.scheduleList.add_widget(Label(text=str(firstTask)))
            self.ids.scheduleList.add_widget(Label(text=EssayHomeworkWindow.steps[0]))
            self.active = CheckBox(active=False)
            self.active.bind(on_release=lambda x: self.checkbox_click(x, x.active, EssayHomeworkWindow.steps[0]))
            self.ids.scheduleList.add_widget(self.active)

            self.ids.scheduleList.add_widget(Label(text=str(secondTask)))
            self.ids.scheduleList.add_widget(Label(text=EssayHomeworkWindow.steps[1]))
            self.active = CheckBox(active=False)
            self.active.bind(on_release=lambda x: self.checkbox_click(x, x.active, EssayHomeworkWindow.steps[1]))
            self.ids.scheduleList.add_widget(self.active)

            self.ids.scheduleList.add_widget(Label(text=str(thirdTask)))
            self.ids.scheduleList.add_widget(Label(text=EssayHomeworkWindow.steps[2]))
            self.active = CheckBox(active=False)
            self.active.bind(on_release=lambda x: self.checkbox_click(x, x.active, EssayHomeworkWindow.steps[2]))
            self.ids.scheduleList.add_widget(self.active)

            self.ids.scheduleList.add_widget(Label(text=str(fourthTask)))
            self.ids.scheduleList.add_widget(Label(text=EssayHomeworkWindow.steps[3]))
            self.active = CheckBox(active=False)
            self.active.bind(on_release=lambda x: self.checkbox_click(x, x.active, EssayHomeworkWindow.steps[3]))
            self.ids.scheduleList.add_widget(self.active)

            self.ids.scheduleList.add_widget(Label(text=str(fifthTask)))
            self.ids.scheduleList.add_widget(Label(text=EssayHomeworkWindow.steps[4]))
            self.active = CheckBox(active=False)
            self.active.bind(on_release=lambda x: self.checkbox_click(x, x.active, EssayHomeworkWindow.steps[4]))
            self.ids.scheduleList.add_widget(self.active)

            self.ids.scheduleList.add_widget(Label(text=str(sixthTask)))
            self.ids.scheduleList.add_widget(Label(text=EssayHomeworkWindow.steps[5]))
            self.active = CheckBox(active=False)
            self.active.bind(on_release=lambda x: self.checkbox_click(x, x.active, EssayHomeworkWindow.steps[5]))
            self.ids.scheduleList.add_widget(self.active)


        elif len(OpenEndedHomeworkWindow.steps) > 0:

            firstTask, secondTask, thirdTask, fourthTask = ScheduleWindow.timeSchedule(self,currentDate,DueDateWindow.homeworkDueDate,currentTime)
            self.ids.scheduleList.add_widget(Label(text=str(firstTask)))
            self.ids.scheduleList.add_widget(Label(text=OpenEndedHomeworkWindow.steps[0]))
            self.active = CheckBox(active=False)
            self.active.bind(on_release=lambda x: self.checkbox_click(x, x.active, OpenEndedHomeworkWindow.steps[0]))
            self.ids.scheduleList.add_widget(self.active)

            self.ids.scheduleList.add_widget(Label(text=str(secondTask)))
            self.ids.scheduleList.add_widget(Label(text=OpenEndedHomeworkWindow.steps[1]))
            self.active = CheckBox(active=False)
            self.active.bind(on_release=lambda x: self.checkbox_click(x, x.active, OpenEndedHomeworkWindow.steps[1]))
            self.ids.scheduleList.add_widget(self.active)

            self.ids.scheduleList.add_widget(Label(text=str(thirdTask)))
            self.ids.scheduleList.add_widget(Label(text=OpenEndedHomeworkWindow.steps[2]))
            self.active = CheckBox(active=False)
            self.active.bind(on_release=lambda x: self.checkbox_click(x, x.active, OpenEndedHomeworkWindow.steps[2]))
            self.ids.scheduleList.add_widget(self.active)

            self.ids.scheduleList.add_widget(Label(text=str(fourthTask)))
            self.ids.scheduleList.add_widget(Label(text=OpenEndedHomeworkWindow.steps[3]))
            self.active = CheckBox(active=False)
            self.active.bind(on_release=lambda x: self.checkbox_click(x, x.active, OpenEndedHomeworkWindow.steps[3]))
            self.ids.scheduleList.add_widget(self.active)




        self.ids.scheduleWindow.remove_widget(self.ids.scheduleGenerator)

    pass


class WindowManager(ScreenManager):
    pass


homeworkDueDate = ""
homeworkType = ""
homeworkTypeOptions = ["essay", "open ended"]
busyTimes = [[], [time(00, 00), time(1, 00), time(2, 00), time(3, 00), time(4, 00), time(5, 00), time(6, 00)]]

# def procedureForOpenEnded():

kv = Builder.load_file("AntiProcrastinator.kv")


class MyGridLayout(Widget):
    age = ObjectProperty(None)


class AntiProcrastinator(App):
    def build(self):
        return kv


if __name__ == "__main__":
    AntiProcrastinator().run()
