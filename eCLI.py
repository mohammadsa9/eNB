import libtmux
import sys
import os

SESSION_Prefix = "eNB"
SESSION_NAME = "default"
SESSION_FULL_NAME = SESSION_Prefix + "_" + SESSION_NAME
server = libtmux.Server()
PWD = os.path.dirname(os.path.realpath(__file__))


def send_cli(session, cli):
    window = session.windows.filter(window_name="default")[0]
    pane = window.panes[0]
    pane.send_keys(cli)


if __name__ == "__main__":
    for index, arg in enumerate(sys.argv):
        if arg == "-i" or arg == "--ip":
            try:
                session = server.new_session(SESSION_FULL_NAME)
                window = session.new_window(attach=False, window_name="default")
                window.split_window(attach=False)
            except:
                print(
                    "Close the previos session before starting another one by typing: "
                )
                print("python3 " + PWD + "/eCLI.py --stop")
                sys.exit()
            if os.path.basename(__file__) == sys.argv[0]:
                final_arguments = " ".join(sys.argv)
            else:
                final_arguments = " ".join(sys.argv[1:])
            send_cli(session, "python3 " + PWD + "/eNB_LOCAL.py " + final_arguments)
            sys.exit()
        if arg == "--stop":
            try:
                server.sessions.filter(session_name=SESSION_FULL_NAME)[0].kill_session()
            except IndexError as e:
                print("Already stopped.")
            sys.exit()
        if arg == "--command":
            session = server.sessions.filter(session_name=SESSION_FULL_NAME)[0]
            print(sys.argv[index + 1])
            send_cli(session, sys.argv[index + 1])
            sys.exit()
