from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume
from argparse import ArgumentParser, RawDescriptionHelpFormatter


class VolumeModifier:
    def __init__(self):
        self.sessions = AudioUtilities.GetAllSessions()

    def list_active_sessions(self):
        for session in self.sessions:
            session_name = session.Process.name() if session.Process else "System Sounds"
            if session_name.endswith(".exe"):
                session_name = session_name[:-4]  # Remove the ".exe" extension
            print("Session Name: %s" % session_name)

    def select_session(self):
        for index, session in enumerate(self.sessions):
            session_name = session.Process.name() if session.Process else "System Sounds"
            if session_name.endswith(".exe"):
                session_name = session_name[:-4]  # Remove the ".exe" extension
            print("%d. %s" % (index + 1, session_name))

        while True:
            selection = input("Select a session by entering its number: ")
            try:
                selection_index = int(selection) - 1
                if 0 <= selection_index < len(self.sessions):
                    return self.sessions[selection_index]
                else:
                    print("Invalid selection. Please enter a valid number.")
            except ValueError:
                print("Invalid selection. Please enter a valid number.")

    def modify_volume(self, session):
        volume = session.SimpleAudioVolume

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

        volume.SetMasterVolume(new_volume, None)
        updated_volume = volume.GetMasterVolume()
        print("Volume updated to: %s" % updated_volume)

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
