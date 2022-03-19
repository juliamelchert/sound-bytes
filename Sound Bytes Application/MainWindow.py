# Author: Julia Melchert
# Date: 2/14/22
# Description: Main UI functionality for SOUND BYTES application 

import sys, os, time

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow

from Ui_MainWindow import Ui_Dialog

class MainWindow():
    """
    Handles operations for the UI window.
    """

    def __init__(self):
        """
        Constructor for the UI window that initializes the window and its widgets' functionalities.
        """
        self.main_win = QMainWindow()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self.main_win)

        # Initializes home page as the first page shown
        self.ui.stackedWidget.setCurrentWidget(self.ui.homePage)

        # Button signals/slots
        self.ui.submitButton.clicked.connect(self.showResults)
        self.ui.helpButton.clicked.connect(self.showHelp)
        self.ui.backButtonR.clicked.connect(self.showHome)
        self.ui.backButtonH.clicked.connect(self.showHome)


    def show(self):
        """
        Displays the main window
        """
        self.main_win.show()


    def showResults(self):
        """
        Shows the results page
        """
        # Gets the user inputs from the "Artist" and "Song" input boxes on the home page.
        artistInput = self.ui.artistInput.toPlainText()
        songInput = self.ui.songInput.toPlainText()

        # Sets the text for the input artist and song
        self.ui.artistBioLabel.setText(f"{artistInput}'s Biography")
        self.ui.songLyricsLabel.setText(f'"{songInput}" Lyrics')
        
        sendRequests(artistInput, songInput)
        
        # Waits for and receives biography and song lyrics from microservices
        self.ui.artistBio.setText(checkFile('../output.txt'))
        self.ui.songLyrics.setText(checkFile('../lyrics-service-output.txt'))

        # Shows the results page
        self.ui.stackedWidget.setCurrentWidget(self.ui.resultsPage)


    def showHome(self):
        """
        Shows the results page
        """
        # Clears the input text
        self.ui.artistInput.setText("")
        self.ui.songInput.setText("")

        # Shows the home page
        self.ui.stackedWidget.setCurrentWidget(self.ui.homePage)


    def showHelp(self):
        """
        Shows the results page
        """
        self.ui.stackedWidget.setCurrentWidget(self.ui.helpPage)


def checkFile(filePath):
    """
    Checks if a file exists. If not, waits until file exists. Once the file exists, the file is read
    and removed, and its contents are returned.
    """
    print("Waiting for response...")
    while os.path.exists(filePath) is False:
        time.sleep(0.1)

    print("Reading response...")
    with open(filePath, 'r') as file:
        fileContents = file.read()

    # Deletes the response file ('../output.txt') so that old responses are not confused with new responses.
    os.remove(filePath)
        
    return fileContents

def sendRequests(artist, song):
    """
    Sends requests to the Wiki Scraper Microservice and Song Lyrics Microservice by writing to specific text files.
    """
    print("Sending requests...")
    # Makes a request to 'signal.txt' to generate the artist's biography with the Wikipedia Scraper Microservice
    with open('../signal.txt', 'w') as biographyRequest:
        biographyRequest.write(f"summary|{artist}")

    # Makes a request to 'lyrics-service-input.txt' to generate the song's lyrics with the Song Lyrics Microservice
    with open('../lyrics-service-input.txt', 'w') as lyricsRequest:
        lyricsRequest.write(f"{artist} {song}")

    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec_())