import cv2
import os
import speech_recognition as sr
import pyttsx3

# Set the directory where you want to save pictures
SAVE_DIR = "G:\Picture"  # Make sure to use forward slashes or double backslashes for paths

# Create the directory if it doesn't exist
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

class CameraAssistant:
    def __init__(self):
        self.camera = None
        self.is_camera_open = False
        self.engine = pyttsx3.init()  # Initialize the text-to-speech engine
        self.engine.setProperty('rate', 150)  # Set speech rate
        self.engine.setProperty('volume', 1)  # Set volume level (0.0 to 1.0)
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[1].id)  # Choose a female or male voice based on index

    def speak(self, text):
        """Use text-to-speech to speak the given text."""
        self.engine.say(text)
        self.engine.runAndWait()

    def open_camera(self):
        """Open the camera for capturing images."""
        if not self.is_camera_open:
            self.camera = cv2.VideoCapture(0)  # Open the camera (0 is usually the default camera)
            if not self.camera.isOpened():
                self.speak("Error: Camera not accessible.")
                print("Error: Camera not accessible.")
                return False
            self.is_camera_open = True
            self.speak("Camera is now open.")
            print("Camera is now open.")
            return True
        else:
            self.speak("Camera is already open.")
            print("Camera is already open.")
            return True

    def close_camera(self):
        """Close the camera and release resources."""
        if self.is_camera_open:
            self.camera.release()  # Release the camera resource
            cv2.destroyAllWindows()  # Close any OpenCV windows
            self.is_camera_open = False
            self.speak("Camera is now closed.")
            print("Camera is now closed.")
        else:
            self.speak("Camera is already closed.")
            print("Camera is already closed.")

    def take_picture(self, filename):
        """Take a picture if the camera is open and save it to the specified filename."""
        if self.is_camera_open:
            ret, frame = self.camera.read()  # Capture a single frame
            if ret:
                cv2.imwrite(filename, frame)  # Save the picture to the file
                self.speak(f"Picture taken and saved as {filename}")
                print(f"Picture taken and saved as {filename}")
            else:
                self.speak("Error: Could not take picture.")
                print("Error: Could not take picture.")
        else:
            self.speak("Camera is not open. Please open the camera first.")
            print("Camera is not open. Please open the camera first.")

    def listen_for_command(self):
        """Listen for a voice command and return it."""
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening for commands...")
            self.speak("Listening for commands.")
            recognizer.adjust_for_ambient_noise(source)  # Adjust for background noise
            audio = recognizer.listen(source)  # Listen to the microphone

        try:
            command = recognizer.recognize_google(audio)  # Use Google's speech recognition
            print(f"You said: {command}")
            return command.lower()  # Convert the command to lowercase
        except sr.UnknownValueError:
            self.speak("Sorry, I could not understand your voice.")
            print("Sorry, I could not understand your voice.")
            return ""
        except sr.RequestError:
            self.speak("Could not request results from Google Speech Recognition service.")
            print("Could not request results from Google Speech Recognition service.")
            return ""

def main():
    """Main logic of the Camera Assistant."""
    assistant = CameraAssistant()  # Create a CameraAssistant object

    while True:
        command = assistant.listen_for_command()  # Listen for a command

        if "open camera" in command:
            assistant.open_camera()  # Open the camera if the command contains "open camera"
        elif "close camera" in command:
            assistant.close_camera()  # Close the camera if the command contains "close camera"
        elif "take a picture" in command:
            # Create a unique filename for the image
            filename = os.path.join(SAVE_DIR, f"image_{len(os.listdir(SAVE_DIR)) + 1}.jpg")
            assistant.take_picture(filename)  # Take a picture
        elif "exit" in command or "quit" in command:
            assistant.close_camera()  # Ensure the camera is closed before exiting
            assistant.speak("Exiting the voice assistant.")
            print("Exiting the voice assistant.")
            break  # Exit the loop and end the program

if __name__ == "__main__":
    main()  # Run the main function if this script is executed
