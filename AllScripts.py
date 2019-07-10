import subprocess

program_list = ['SubjectSelectorDirectory.py', 'ActivitySequenceCounter.py']

for program in program_list:
    subprocess.call(['python', program])
    print("Finished:" + program)