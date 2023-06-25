"""
This script allows modifying the volume of active audio sessions.

needed:
    - pycaw: Python bindings for Core Audio Windows API
    - argparse: Library for parsing command-line arguments
    - colorama: Cross-platform library for colored terminal text

Usage:
    - View help arg
"""
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from pycaw.pycaw import AudioUtilities
from colorama import init, Fore

# Init colors
init()


class VolumeModifier:
    """
    Class for modifying the volume of active audio sessions.
    """
    def __init__(self):
        self.sessions = AudioUtilities.GetAllSessions()

    def list_active_sessions(self):
        """
        Function to  list active session
        """
        for index, session in enumerate(self.sessions):
            session_name = session.Process.name() if session.Process else "System Sounds"
            if session_name.endswith(".exe"):
                session_name = session_name[:-4]  # Remove the ".exe" extension
            session_volume = session.SimpleAudioVolume.GetMasterVolume()
            volume_percentage = int(session_volume * 100)
            volume_color = self.get_volume_color(session_volume)
            print(f"{index + 1}. {session_name} (Volume: "
                f"{volume_color}{volume_percentage}%{Fore.RESET})")


    def select_session(self):
        """
        allow user to select the right session in order to modify volume value
        """
        while True:
            selection = input("Select a session by entering its number (or 'q' to quit): ")
            if selection.lower() == 'q':
                return None
            try:
                selection_index = int(selection) - 1
                if 0 <= selection_index < len(self.sessions):
                    session = self.sessions[selection_index]
                    session_volume = session.SimpleAudioVolume.GetMasterVolume()
                    if session_volume > 0.0:
                        return session
                    print(f"{Fore.LIGHTRED_EX}Selected session is not currently producing sound."
                          f"Please choose another session.{Fore.RESET}")
                else:
                    print(f"{Fore.LIGHTRED_EX}Invalid selection."
                        f"Please enter a valid number.{Fore.RESET}")
            except ValueError:
                print(f"{Fore.LIGHTRED_EX}Invalid selection."
                    f"Please enter a valid number.{Fore.RESET}")

    def modify_volume(self, session):
        """
        Allow to modify the volume of a specified and selected session.
        """
        if session is None:
            return

        volume = session.SimpleAudioVolume

        while True:
            new_volume = input("Enter the new volume value (0 to 100): ")
            if new_volume.lower() == 'q':
                return
            try:
                new_volume = int(new_volume)
                if 0 <= new_volume <= 100:
                    break
                print(f"{Fore.LIGHTRED_EX}Invalid volume value."
                      f"Please enter a value between 0 and 100.{Fore.RESET}")
            except ValueError:
                print(f"{Fore.LIGHTRED_EX}Invalid volume value."
                    f"Please enter a valid number.{Fore.RESET}")

        volume.SetMasterVolume(new_volume / 100, None)
        updated_volume = volume.GetMasterVolume()
        volume_percentage = int(updated_volume * 100)
        volume_color = self.get_volume_color(updated_volume)
        print(f"Volume updated to: {volume_color}{volume_percentage}%{Fore.RESET}")

    @staticmethod
    def get_volume_color(volume):
        """
        define color of volume compared to pourcent
        """
        if volume <= 0.3:
            return Fore.GREEN  # Vert
        if volume <= 0.7:
            return Fore.YELLOW  # Jaune
        return Fore.RED  # Rouge

    def run(self):
        """
        Run function
        """
        self.list_active_sessions()
        session = self.select_session()
        self.modify_volume(session)


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

    volume_modifier = VolumeModifier()
    volume_modifier.run()
