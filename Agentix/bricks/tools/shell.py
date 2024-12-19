from time import sleep
from collections import defaultdict
from rich import print
import re
import time
import string
import random
from agentix import tool, Tool, State
import subprocess


@tool
def shell(command: str) -> str:
    """
    Executes a shell command and returns the result.

    Args:
        command (str): The command to execute in the shell.

    Returns:
        str: The output from the shell command.
    """
    result = subprocess.run(
        command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        return f"Error: {result.stderr}"
    return result.stdout


def ensure_tmux_session(session_name: str):
    try:
        subprocess.run(["tmux", "has-session", "-t", session_name], check=True)
    except subprocess.CalledProcessError:
        subprocess.run(["tmux", "new-session", "-d", "-s", session_name])


def generate_marker():
    """Generate a unique marker string"""
    random_str = ''.join(random.choices(
        string.ascii_uppercase + string.digits, k=20))
    return f"COMMAND_MARKER_{random_str}_START"


def get_pane_content(session_name: str):
    """Get the current content of the tmux pane"""
    result = subprocess.run(["tmux", "capture-pane", "-p", "-t", session_name],
                            capture_output=True, text=True, check=True)
    return result.stdout.split('\n')


def wait_for_command_completion(session_name: str, marker: str, timeout: int = 60):
    """Wait for command completion by monitoring terminal output"""
    previous_content = None
    stable_count = 0
    start_time = time.time()

    while time.time() - start_time < timeout:
        current_content = get_pane_content(session_name)

        # Find marker position
        try:
            marker_index = next(i for i, line in enumerate(
                current_content) if marker in line)
        except StopIteration:
            time.sleep(0.5)  # Short sleep if marker not found yet
            continue

        # Get content after marker
        content_after_marker = current_content[marker_index + 1:]

        # If content is same as previous check
        if content_after_marker == previous_content:
            stable_count += 1
            if stable_count >= 2:  # Content stable for 2 checks (6 seconds)
                return content_after_marker
        else:
            stable_count = 0

        previous_content = content_after_marker
        time.sleep(3)

    raise TimeoutError(f"Command execution timed out after {timeout} seconds")


@tool
def execute_shell_command(command: str, session_name: str = "Shella", n: int = -1, timeout: int = 60) -> str:
    """
    Execute a shell command in a tmux session and return the output.

    Args:
        command: The command to execute
        session_name: The name of the tmux session to use
        n: Number of lines to return (-1 for all lines after marker)
        timeout: Maximum time to wait for command completion in seconds

    Returns:
        Command output as string

    Raises:
        TimeoutError: If command execution exceeds timeout
        subprocess.CalledProcessError: If tmux commands fail
    """
    ensure_tmux_session(session_name)

    # Generate and send marker
    # marker = generate_marker()
    # subprocess.run(["tmux", "send-keys", "-t", session_name, f"echo '{marker}'", "C-m"],
    #               check=True)

    # Send the actual command
    subprocess.run(["tmux", "send-keys", "-t", session_name, command, "C-m"],
                   check=True)

    # Wait for command completion
    try:
        output_lines = wait_for_command_completion(
            session_name, marker, timeout)
    except TimeoutError as e:
        raise TimeoutError(
            f"Command '{command}' timed out after {timeout} seconds")

    # Remove empty lines at the start and end
    output_lines = [line for line in output_lines if line.strip()]

    if not output_lines:
        return ""

    # Process output based on n parameter
    if n == -1:
        return '\n'.join(output_lines).strip()
    else:
        return '\n'.join(output_lines[-n:]).strip()


_Output_Buffers = defaultdict(list)


@tool
def run_with_tmux(command: str | bool, session_name: str) -> str:
    global _Output_Buffers
    socket = "/tmp/mytmux.sock"

    def gather_pane_content():
        # Mi bredren, dis yah function yah fi gather di current tmux content
        result = subprocess.run(["tmux", "capture-pane",  "-pS -10000", "-t",
                                session_name], capture_output=True, text=True, check=True)
        return result.stdout.split('\n')

    # Ensure seh wi have a tmux session ready fi use
    ensure_tmux_session(session_name)

    def run_cmd(cmd: str):
        if cmd is not False:
            subprocess.run(["tmux", "send-keys", "-t", session_name,
                            cmd, "C-m"], check=True)

    run_cmd(command)
    sleep(1)

    last_lines = []  # Remember di last few lines wi see
    ttl = 50
    while True:
        # Tek a likkle breather fi mek di command execute
        current_content = gather_pane_content()

        # print(current_content)
        # input('a')
        # print(_Output_Buffers[session_name])
        # input('b')
        moar_buffer = []
        l = len(current_content)

        all_empty = True
        for line in current_content[::-1]:
            if (len(line.strip())):
                all_empty = False
                break
        '''
        if all_empty:
            print(current_content)
            # print('empty')
            ttl -= 1
            sleep(.1)
            if ttl <= 0:
                run_cmd('')
                ttl = 50
                sleep(.5)
            continue

        putall = len(_Output_Buffers[session_name]) == 0
        bibou = _Output_Buffers[session_name]
        if not all_empty and putall:
            # print('setting initial state of buffer')
            _Output_Buffers[session_name] = [
                l for l in current_content if len(l.strip())]
            continue

        for i, line in enumerate(current_content[::-1]):
            # print(f'[blue]LLL{i}/{l}', line)
            if line.strip() == '':
                # print('dada')
                continue

            if (len(_Output_Buffers[session_name]) and line.strip() == _Output_Buffers[session_name][-1].strip()) \
                    or (i >= (l-1)):
                # print('add buffer', moar_buffer)
                _Output_Buffers[session_name] += moar_buffer
                break
            # print('[red] new line !')
            # print(line)
            # print('add to buffa:[red]xXxXx[/]:', line)
            moar_buffer = [line] + moar_buffer

        time.sleep(.1)

        if _Output_Buffers[session_name] == [] or len(_Output_Buffers[session_name]) == 0:
            if ttl == 50:
                print('\t\t    [red]TTL')
                print(current_content)
            ttl -= 1
            sleep(.2)
            print(f"{ttl=}  ", end='\r')
            if ttl <= 0:
                run_cmd('')
                print('sending enter to refresh the pane')
                sleep(1)
                ttl = 50
            continue
        else:
            ttl = 50
        '''
        # If wi see di prompt again, di command done
        # print('we here')

        curcont = gather_pane_content()
        break_loop = False
        for i in range(1, len(curcont)):

            time.sleep(.05)
            # print(f'FYI: {-i}',
            #      f"{curcont[-i].strip()=}")
            if curcont[-i].strip() == '':
                # print('skip')
                continue
            last_line = curcont[-i].strip()
            if last_line.startswith('➜') or last_line in ['>', 'ask>']:
                break_loop = True
                # print('break loop')
                break
            # print('non')
            break

        # Update di last lines wi remember fi next time
        last_lines = current_content[-3:]
        if break_loop:
            break
    # input('de end')
    # Join up all di lines fi return di final output
    from copy import deepcopy
    ob = gather_pane_content()
    while ob[-1].strip() == '':
        ob.pop()
    if ob[-1].strip().endswith('✗'):
        return ob[:-1]
    return ob


@ tool
def get_session_state(session: str):
    run_with_tmux('', session)
    sleep(0.5)
    run_with_tmux('', session)
    sleep(0.5)

    run_with_tmux('', session)
    sleep(.2)
    return run_with_tmux(False, session)


def is_unix_path(path_string):
    # Pattern explanation:
    # ^           - Start of string
    # /?          - Optional leading slash
    # (           - Start of group
    #   [a-zA-Z0-9_\-\.]+ - One or more alphanumeric chars, underscore, dash, or dot
    #   /?        - Optional slash
    # )*          - Zero or more occurrences of the group
    # $           - End of string
    pattern = r'^/?([a-zA-Z0-9_\-\.]+/?)*$'
    return bool(re.match(pattern, path_string))


@ tool
def is_aider(session: str):
    return get_session_state(session)[-1].strip() in ['>', 'ask>']


@ tool
def get_aider_files(session: str):
    if not is_aider(session):
        raise Exception(f'{session} does not seem to be running aider')

    state = get_session_state(session)
    state.pop()
    files = []
    for line in state:
        if is_unix_path(line.strip()):
            files.append(line.strip())
        else:
            return files
    return files


@tool
def Human(msg):
    return Tool['talk_to_agent'](msg, agent_name='Human')


@ tool
def _aider_project(project_name: str) -> dict:
    # TODOX: I want to be able to do State["SomeStateThatDoesntExistYet"]['some_key'] = 'bla' and State will simple assume a dict.
    # TODOX: I want that states of relevance have doc.
    """TODOx:
    State['StateDoc']['projects'] = '''
    structure and values and stuff.
'''
    """

    # TODOX: I want a widget with console like feel where I can type commands like see the dump of a state.

    if not "projects" in State or (State['projects'].to_dict() == {}):
        State['projects'] = {
            "current": project_name,
            'projects': {}
        }
    State['projects']['current_project'] = project_name

    def iter_input(msg):
        values = []
        while True:
            val = Tool['Human'](
                f"I'm setting up `{project_name}`\ngive me {msg} plz. One per line or one per message. \nJust send '.' and nothing else to continue")
            if val.strip() == '.':
                break
            for v in val.split('\n'):
                values += [v.strip]
        return values

    if not project_name in State['projects']['projects']:

        State['projects']['projects'][project_name] = {
            'base_dir': input('base dir ?'),
            'files_to_add': iter_input('path to add'),
            'files_to_drop': iter_input('path to drop'),
        }

    state_dict = State['projects']['projects'][project_name].to_dict()
    base_dir = state_dict['base_dir']
    files_to_add = state_dict['files_to_add']
    files_to_drop = state_dict['files_to_drop']

    o_sess_name = f'{project_name}_omni'
    if not is_aider(o_sess_name):
        print('init omni aider')
        run_with_tmux(f"cd {base_dir}", o_sess_name)

        time.sleep(.05)
        run_with_tmux(f"aider --sonnet --no-pretty", o_sess_name)
        # run_with_tmux('aider --model ollama_chat/qwq --no-pretty', o_sess_name)
        # time.sleep(1)
        print('sending <Enter> a bunch of times')
        for i in range(5):
            run_with_tmux('', o_sess_name)
            # time.sleep(0.02)

        run_with_tmux('/chat-mode ask', o_sess_name)

        for path in files_to_add:
            print(f"/add {path}")
            run_with_tmux(f"/add {path}", o_sess_name)
            # time.sleep(0.5)

        for path in files_to_drop:
            print(f"/drop {path}")
            run_with_tmux(f"/drop {path}", o_sess_name)
            # time.sleep(0.5)

    assert is_aider(
        o_sess_name), f"something went wrong wrapping aider in tmux session `{o_sess_name}`"
    State['projects']['projects'][project_name]['aider_session']['omni'] = o_sess_name

    return State['projects']['projects'][project_name]


@ tool
def all_aider_sessions(project_name: str) -> list[str]:
    return State['projects']['projects'][project_name]['aider_session']


@tool
def random_id():
    adjectives = [
        "Glorious", "Mighty", "Swift", "Clever", "Brave", "Fierce", "Wise",
        "Noble", "Silent", "Wild", "Gentle", "Bold", "Ancient", "Mystic",
        "Agile", "Nimble", "Radiant", "Valiant", "Elegant", "Graceful",
        "Fearless", "Dashing", "Ethereal", "Majestic", "Legendary", "Epic",
        "Heroic", "Dynamic", "Stellar", "Cosmic", "Thundering", "Blazing",
        "Mysterious", "Enigmatic", "Powerful", "Unstoppable", "Incredible",
        "Fantastic", "Magnificent", "Spectacular", "Brilliant", "Dazzling",
        "Remarkable", "Enchanted", "Magical", "Celestial", "Imperial", "Grand",
        "Supreme", "Ultimate", "Infinite", "Eternal", "Immortal", "Divine",
        "Sacred", "Blessed", "Mighty", "Fearsome", "Savage", "Primal",
        "Untamed", "Feral", "Fierce", "Ferocious", "Vigilant", "Watchful",
        "Keen", "Sharp", "Cunning", "Shrewd", "Astute", "Clever", "Wise"
    ]

    names = [
        "Lion", "Eagle", "Wolf", "Dragon", "Tiger", "Bear", "Falcon",
        "Snake", "Panther", "Fox", "Hawk", "Owl", "Phoenix", "Dolphin",
        "Leopard", "Jaguar", "Lynx", "Cheetah", "Cougar", "Puma", "Caracal",
        "Serval", "Ocelot", "Wildcat", "Mongoose", "Badger", "Wolverine",
        "Raven", "Crow", "Condor", "Vulture", "Osprey", "Harrier", "Kite",
        "Kestrel", "Merlin", "Peregrine", "Goshawk", "Buzzard", "Griffin",
        "Hydra", "Basilisk", "Wyvern", "Manticore", "Sphinx", "Chimera",
        "Kraken", "Leviathan", "Behemoth", "Unicorn", "Pegasus", "Hippogriff",
        "Thunderbird", "Salamander", "Serpent", "Viper", "Python", "Cobra",
        "Mamba", "Anaconda", "Boa", "Rattler", "Adder", "Krait", "Asp",
        "Scorpion", "Spider", "Mantis", "Beetle", "Dragonfly", "Butterfly",
        "Stallion", "Mustang", "Coyote", "Jackal", "Dingo", "Hyena",
        "Rhino", "Elephant", "Gorilla", "Orangutan", "Gibbon", "Mandrill",
        "Shark", "Whale", "Orca", "Narwhal", "Swordfish", "Barracuda",
        "Octopus", "Squid", "Nautilus", "Turtle", "Tortoise", "Iguana",
        "Monitor", "Komodo", "Gecko", "Chameleon", "Pangolin", "Armadillo",
        "Mammoth", "Sabertooth", "Raptor", "Rex", "Pterodactyl", "Stegosaurus",
        "Ram", "Bison", "Buffalo", "Moose", "Elk", "Stag", "Antelope",
        "Gazelle", "Impala", "Kudu", "Oryx", "Ibex", "Markhor", "Tahr"
    ]

    return f"{random.choice(adjectives)}{random.choice(names)}"


@tool
def __insure_aider(session_name: str, name: str | bool = False) -> bool:
    if is_aider(session_name):
        return True
    name = name or session_name
    project_name = State['projects']['current']
    base_dir = State['projects']['projects'][project_name]['base_dir']
    run_with_tmux(f"cd {base_dir}", session_name)
    # State['projects']['projects'][project_name]['aider_session'][name] = session_name
    run_with_tmux('aider --sonnet --no-pretty', session_name)
    # run_with_tmux('aider --model ollama_chat/qwq --no-pretty', session_name)
    print(f"setting up aider session: [green b]{session_name}[/]", end="")
    while not is_aider(session_name):
        print('.', end='')
    return False


@tool
def set_context_files(session_name: str, paths: list[str]):
    assert is_aider(
        session_name), f"You should run `Tool['insure_aider']({session_name})` first"

    run_with_tmux('/drop', session_name)
    run_with_tmux(f"/add {' '.join(paths)}")


@tool
def talk_to_actor(session_name: str, message: str) -> dict[str, str]:
    # TODO: add CoT
    prompt = f"""
    """


@tool
def ____talk_to_omni(message):
    # return 'oiu'
    project = State['projects']['current_project']

    if input(f"Current project is {project}, continue ? (Y)/n: ").strip().startswith('n'):
        print('bye then')
        return
    all_sessions = all_aider_sessions(project)

    assert 'omni' in all_sessions, f'init project with \nTool["_aider_project"]("{project}")\n'
    o_sess = all_sessions['omni']
    reply_name = random_id()
    assert is_aider(o_sess), f"{o_sess} doesn't seem like an aider session"
    run_with_tmux('/chat-mode ask', o_sess)
    full_msg = f"""
## **Output Format**
You'll think about the problem using <thought ttl="n">your thought</thought>
The reply should be inside <reply></reply>.

Your base ttl is given at the start, you're allowed that many thoughts.
- If you're asked for a list of files, you reply should consist in file paths and nothing else, one per line.
- If you're ask for a list of file, be greedy and add, if possible, extra files where stuff looks like what we want to do for inspiration/convention

Here's an example of output:
```
user: Can you give me the list of relevant files to add a module ?
assistant:<thought ttl="25">I should find the doc for modules</thought>
<thought ttl="24">I should also include some already implemented module for inspiration</thought>
...
<thought ttl="2">User asked for a list of files, my reply should be easily parsable, I'll answer with file paths, one per line and nothing else</thought>

<reply name="GloriousPimple">
modules/doc.md
modules/SomeModule/manifest.yml
...
</reply>

The thing we'll work on today
## **User question**

{message}

## **Settings**

- Your thought TTL is 27
- The `name` attr of your reply opening tag should be '{reply_name}'
    """
    with open('/tmp/zouzou', "w") as f:
        f.write(full_msg)

    run_with_tmux('wl-copy < /tmp/zouzou', 'zoubida')

    reply = '\n'.join(run_with_tmux('/paste', o_sess))
    reply_content = Tool['xml_parser']('reply')(
        reply).get(reply_name, {}).get('content', '')

    return reply_content


@tool
def list_relevant_files(task_description: str = '') -> list[str]:

    return talk_to_omni(task_description).split('\n')
