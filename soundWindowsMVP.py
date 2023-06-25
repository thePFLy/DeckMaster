from __future__ import print_function
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume
from argparse import ArgumentParser, RawDescriptionHelpFormatter


def listActiveSession():
    # Get all executed audio sessions
    sessions = AudioUtilities.GetAllSessions()
    # Flag to track if a matching session is found
    match_found = False
    # Browse audio sessions
    for session in sessions:
        # Get the display name of the session
        session_name = session.Process.name() if session.Process else "System Sounds"
        # Check if the session name ends with ".exe"
        if session_name.endswith(".exe"):
            session_name = session_name[:-4]  # Remove the ".exe" extension
        # Display the name of the session
        print("Session Name: %s" % session_name)
    

def sessionSelection():
    # Get all executed audio sessions
    sessions = AudioUtilities.GetAllSessions()
    
    # Display the list of active sessions
    for index, session in enumerate(sessions):
        session_name = session.Process.name() if session.Process else "System Sounds"
        if session_name.endswith(".exe"):
            session_name = session_name[:-4]  # Remove the ".exe" extension
        print("%d. %s" % (index + 1, session_name))
    
    # Prompt the user to select a session
    while True:
        selection = input("Select a session by entering its number: ")
        try:
            selection_index = int(selection) - 1
            if 0 <= selection_index < len(sessions):
                return sessions[selection_index]
            else:
                print("Invalid selection. Please enter a valid number.")
        except ValueError:
            print("Invalid selection. Please enter a valid number.")


def modifyVolume(session):
    # Get the volume control of the session
    volume = session.SimpleAudioVolume
    
    # Prompt the user to enter a new volume value
    while True:
        new_volume = input("Enter the new volume value (0.0 to 1.0): ")
        try:
            new_volume = float(new_volume)
            if 0.0 <= new_volume <= 1.0:
                break
            else:
                print("Invalid volume value. Please enter a value between 0.0 and 1.0.")
        except ValueError:
            print("Invalid volume value. Please enter a valid number.")
    
    # Set the new volume value
    volume.SetMasterVolume(new_volume, None)
    
    # Display the updated volume value
    updated_volume = volume.GetMasterVolume()
    print("Volume updated to: %s" % updated_volume)




def main():
    listActiveSession()
    session = sessionSelection()
    modifyVolume(session)

if __name__ == '__main__':
    parser = ArgumentParser(
        formatter_class=RawDescriptionHelpFormatter,
        description='''
    Help description\n
    ----------------------\n
    1. Read the list of all volume application\n
    2. Select one of them to modify\n
    3. Change the volume\n
    ''')
    args = parser.parse_args()
    main()
