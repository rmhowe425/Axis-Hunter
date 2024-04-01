from src.IO import IO
from src.AudioVideo import AudioVideo


def main():
    base_url = ''
    commands = {
        'IO': IO,
        'Audio & Video': AudioVideo
    }

    for command in commands:
        command_inst = commands[command](base_url)
        print(f'{command}\n{"="*10}\n{command_inst.print_results()}')


main()
