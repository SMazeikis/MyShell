# Use Python 3

import os
import getpass
import socket
import pathlib
import sys
# import readline
import threading
import platform
from subprocess import *

def main():
	# if the shell is called with 2 arguments for i/o redirection, proceed to seperate them into a list and execute them appropriately.
	if len(sys.argv) == 2:
		execute(sys.argv[1:])
	# otherwise get all the relevant information for the command line interface and wait for input,
	while True:
		USER = getpass.getuser()
		HOST = socket.gethostname()
		CWD = os.getcwd()
        # waits for input while displaying needed information.
		line = input(USER + HOST + CWD +"  --> ".strip())
		args = line.split()
		execute(args)


def execute(args):
	# argument order is important, as ampersand has to be checked first so other commands don't jump infront, and where order is not needed attempted to be ordered by the most frequent use.
	try:
		# if there is no arguments and only "enter" has been pressed, go back to the main loop waiting for input.
		if len(args) == 0:
			pass

		# check first if ampersand has been inputed as it is the most important check  for it to be turned into a background process.
		elif args[-1] == "&":
			background_process = threading.Thread(target=execute, args=(args[:-1],))
			background_process.start()

		elif ">" in args or ">>" in args:
			# backups the original sys.stdout to bring back after finishing output to file so user can print out in terminal.
			backup = sys.stdout
			output = args[-1]
			# have to first check for double >> as to insure that it is append and not write over.
			if ">>" in args:
				sys.stdout = open(output, "a")
			elif ">" in args:
				sys.stdout = open(output, "w")
			# if python make sure to go into seperate statement as to complete python process, all commands done under subprocess.
			if "python" in args[0]:
				first_process = Popen(args[:2], stdin = PIPE, stdout = sys.stdout)
				first_process.communicate()
                # if the last input has a python extension open it again and process it.
				if args[2][-3:] == ".py":
					second_process = Popen(args[:1] + args[2:3], stdin = PIPE, stdout = sys.stdout)
					second_process.communicate()
			else:
                # if python is not found in the argument execute it normally.
				execute(args[:-2])
			# return sys.stdout from backup as user would think it would work like.
			sys.stdout = backup

		# check if the file is a batch file, which most endings end with bat, cmd, or bsm.
		elif args[0][-3:] in ["bat","cmd","bsm"]:
			# open the batch file and go into executing the appropriate commands in my own execution function.
			batch = open(r'{}/{}'.format(os.getcwd(), "".join(args)), "r")
			for line in batch:
				line = line.split()
				execute(line)
			# quit once done the batch file.
			execute(["quit"])

		elif "echo" == args[0]:
			if len(args) == 1:
				print("\n")
			else:
				# gets rid of spaces and ensures to join the arguments by one space.
				print(" ".join(args[1:]))

		elif "cd" == args[0]:
			# go to function cd for processing of the command
			args = "".join(args[1:])

			try:
				# attempt to check if no directory has been selected to go into, if so, list the current directory files and directories.
				if len(args) == 0:
					home_directory = str(os.getcwd()).strip()
					os.chdir(home_directory)
					print(home_directory)
				# otherwise, take the full path of the directory and list the appropriate contents of it.
				else:
					os.chdir(args)
			
			except Exception as e:
				# the user has entered a path which is not entirely correct, or does not exist.
				print("cd: no such file or directory: " + args)

		elif "dir" == args[0]:
			# check if only dir contained, if so list the files and working directorys of current directory.
			if len(args) == 1:
				files = [f for f in os.listdir(os.getcwd()) if not f[0] == "."]
			# else list the path specified and make sure there are files and current working directories and not ant useless files.
			else:
				files = [f for f in os.listdir(args[1]) if not f[0] == "."]
			for f in files:
				print(f, end = "  ")
			print("\n")

		elif "clr" == args[0]:
			# check first what platform is being used.
			if platform.system() == "Windows":
				os.system("cls")
			else:
				# allows to clear the current screen without using os commands.
				print("\x1b[2J\x1b[H",end="")

		elif "pause" == args[0]:
			# wait for enter to be pressed as that's the only thing to continue the process.
			input("Please press ENTER to unpause\n")

		elif "environ" == args[0]:
			# lists the current information about the environment from the dictionary environ
			if len(args) == 1:
				for k, v in os.environ.items():
					print(k + ":" + "\n" + v + "\n")
			else:
				print("environ: Incorrect use of Command")

		elif "help" == args[0]:
			manual = open("readme", "r")
			# manual = manual.readlines()
			# start at line 4 as the others are my name and student number, outside loop because we don't want to reset the current location.
			i = 3
			while True:
				# j keeps track of how many lines have been printed out.
				j = 0
				while j < 25:
					try:
						print(manual[i].strip())
					except IndexError:
						# once it reaches end of manual, go back to main and await input.
						main()
					i += 1
					j += 1
				# waits for persons input.
				command = input("...")
				if command == "q":
					break

		elif "quit" == args[0]:
			raise SystemExit

		else:
			# takes care of any other commands that are not declared by my shell, and if the user typed in incorrectly declares that there is no such command.
			process = os.fork()
			if pid > 0:
				working_process = os.waitpid(pid, 0)
			else:
				try:
					os.execvp(args[0], args)
				except Exception as e:
					print("sesh: command not found: " + args[0])

	except EOFError as e:
		# no input was found.
		print("EOFError: input was empty")


if __name__ == '__main__':
	main()