from rich import print
import os
import glob

from .instances_store import InstancesStore
from .middleware import MW, mw
from .tool import Tool, tool
from agentix.entities import Conversation
oprint = print

_DEBUG = os.getenv('AGENTIX_DEBUG')


class Agent(metaclass=InstancesStore):
    def __init__(self, name: str, middlewares: str):
        """
        Initialize a new Agent instance.

        :param name: The name of the Agent.
        :param middlewares: A list of middleware instances to be used by the Agent.
        :raises Exception: If an Agent with the given name already exists.
        """
        _DEBUG and print(
            f"init Agent [green b]{name}[/] with [blue i]{middlewares}")
        # FIXME: Actually implement logs
        self.name = name

        # if name in Agent:
        #    raise Exception(f"Agent with name '{name}' already exists.")

        Agent[name] = self
        self._middlewares_str = middlewares

    @property
    def base_prompt(self):
        grandparent_path = os.getcwd()
        pattern = grandparent_path + f"/**/prompts/{self.name}.conv"

        for file_path in glob.glob(pattern, recursive=True):
            self._histo_path = file_path.replace(
                '/prompts/', '/prompts/.histo/')
            histo_dir = os.path.dirname(self._histo_path)
            if not os.path.exists(histo_dir):
                os.makedirs(histo_dir, exist_ok=True)
            return Conversation.from_file(file_path)

        raise FileNotFoundError(f"Did not find {self.name}.conv")

    @property
    def histo(self):
        try:
            return Conversation.from_file(self._histo_path)
        except:  # FIXME: have typed exception & exception handling, this can hide nasty bugs
            return Conversation([])

    def append_histo(self, msg):
        try:
            last = self.histo[-1]
            if last.content == msg.content and last.role == msg.role:
                return
        except:  # FIXME
            pass
        (self.histo + msg).to_file(self._histo_path)

    def __repr__(self):
        return f"Agent({self.name}):\t" + ' -> '.join([f"{mw}" for mw in self._middlewares])

    def __call__(self, *args, **kwargs):
        """
        """
        if self.name == 'Null':
            return f"I'm {self.info}. I don't exist yet though, that's a null pattern branch to tell you you should implement it."

        self._middlewares = [MW[name.strip()]
                             for name in self._middlewares_str.split('|')]
        from agentix import Exec
        ctx = {
            'exec': Exec.get_instance(),
            'agent': self,
            'args': args,
            'hops': 0,
            'kwargs': kwargs,
            "base_discord_message_id": kwargs.get('user_discord_message_id', "-1"),
            "discord": {},
        }  # 'agent': self, 'input': args, 'hops':0}

        conv = args
        current_project_message = None
        for mware in self._middlewares:
            dada1 = getattr(conv, 'discord', 'nope')
            if isinstance(conv, Conversation) and not hasattr(conv, 'discord'):
                conv.discord = {"base": kwargs.get(
                    'user_discord_message_id', '-1')}
            dada2 = getattr(conv, 'discord', 'nope')
            if type(conv) is tuple:
                conv = mware(ctx, *conv)
            else:

                dada3 = getattr(conv, 'discord', 'nope')
                conv = mware(ctx, conv)
                if isinstance(conv, Conversation) and not hasattr(conv, 'discord'):
                    conv.discord = {"base": kwargs.get(
                        'user_discord_message_id', '-1')}
                dada4 = getattr(conv, 'discord', 'nope')
            dism = kwargs.get("discord_message_id", "-1")
            while isinstance(conv, Conversation) and conv.should_infer:

                dada5 = getattr(conv, 'discord', 'nope')
                # print(f"🤖[blue u b]{self.name}[/]_____\n{conv[-3:]}")
                # FIXME add a method that doesn't set should_infer to True
                self.append_histo(conv[-1])
                print(f"{conv.llm=}")
                tool_to_use = 'llm' if not conv.llm.startswith(
                    'o1') else "llm_no_stream"

                if "aider" in conv.llm:
                    tool_to_use = conv.llm + '_tool'
                dada6 = getattr(conv, 'discord', None)
                conv = conv.rehop(
                    Tool[tool_to_use](conv),
                    'assistant'
                )
                if dada6 and not hasattr(conv, 'discord'):
                    conv.discord = dada6
                dada7 = getattr(conv, 'discord', 'nope')

                # TODO: allow conv.rehop(model="gpt-3.5-turbo")
                content = conv
                if isinstance(conv, Conversation):
                    content = conv[-1].content
                    role = conv[-1].role
                Tool['HF_send_message'](f"""■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■                                    
### Agent {self.name}: ({role}):
<content>
{content} 
</content>""", 'debug')
                self.append_histo(conv[-1])
                ctx['hops'] += 1
                conv.should_infer = False
                dada8 = getattr(conv, 'discord', None)
                conv = mware(ctx, conv)
                if isinstance(conv, Conversation) and dada8 and not hasattr(conv, 'discord'):
                    conv.discord = dada8
                dada9 = getattr(conv, 'discord', 'nope')

        return conv

    def clear_histo(self):
        """Clears the history by saving an empty Conversation."""
        Conversation([]).to_file(self._histo_path)

    def __repr__(self):
        return f"Agent['{self.name}']"

    def setinfo(self, info):
        self.info = info


Agent('Null', '')
