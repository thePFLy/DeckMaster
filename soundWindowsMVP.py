from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume
from argparse import ArgumentParser, RawDescriptionHelpFormatter


class VolumeModifier:
    def __init__(self):
        self.sessions = AudioUtilities.GetAllSessions()

    def list_active_sessions(self):
        for index, session in enumerate(self.sessions):
            session_name = session.Process.name() if session.Process else "System Sounds"
            if session_name.endswith(".exe"):
                session_name = session_name[:-4]  # Remove the ".exe" extension
            session_volume = session.SimpleAudioVolume.GetMasterVolume()
            volume_percentage = int(session_volume * 100)
            print("%d. %s (Volume: %d%%)" % (index + 1, session_name, volume_percentage))

    def select_session(self):
        while True:
            selection = input("Select a session by entering its number: ")
            try:
                selection_index = int(selection) - 1
                if 0 <= selection_index < len(self.sessions):
                    session = self.sessions[selection_index]
                    session_volume = session.SimpleAudioVolume.GetMasterVolume()
                    if session_volume > 0.0:
                        return session
                    else:
                        print("Selected session is not currently producing sound. Please choose another session.")
                else:
                    print("Invalid selection. Please enter a valid number.")
            except ValueError:
                print("Invalid selection. Please enter a valid number.")

    def modify_volume(self, session):
        volume = session.SimpleAudioVolume

        while True:
            new_volume = input("Enter the new volume value (0 to 100): ")
            try:
                new_volume = int(new_volume)
                if 0 <= new_volume <= 100:
                    break
                else:
                    print("Invalid volume value. Please enter a value between 0 and 100.")
            except ValueError:
                print("Invalid volume value. Please enter a valid number.")

        volume.SetMasterVolume(new_volume / 100, None)
        updated_volume = volume.GetMasterVolume()
        volume_percentage = int(updated_volume * 100)
        print("Volume updated to: %d%%" % volume_percentage)

    def run(self):
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
