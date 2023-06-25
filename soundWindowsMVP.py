from __future__ import print_function
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume


def main():
    # Get all executed audio sessions
    sessions = AudioUtilities.GetAllSessions()
    # Flag to track if a matching session is found
    match_found = False
    # Browse audio sessions
    for session in sessions:
        # Display executed audio session
        print(session)
        # Get "ISimpleAudioVolume" interface to adjust volume
        volume = session._ctl.QueryInterface(ISimpleAudioVolume)
        # Verify if specified audio session corresponds to Discord
        if session.Process and session.Process.name() == "Discord.exe":
            # Current volume value of the session
            print("volume.GetMasterVolume(): %s" % volume.GetMasterVolume())
            # Set new volume value
            volume.SetMasterVolume(0.65, None)
            # Set the flag to indicate a match is found
            match_found = True
    # Check if no matching session is found
    if not match_found:
        print("\033[91mInactive session\033[0m")


if __name__ == "__main__":
    main()
