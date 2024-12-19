from agentix import mw, Message, Tool

@mw
def prompt(ctx, input_str): 
    return ctx['agent'].base_prompt + Message(role='user', content=input_str)


@mw
def prompt_histo(ctx, input_str):
    base_prompt = ctx['agent'].base_prompt
    ctx['user_input'],*_ = ctx['args']

    histo = ctx['agent'].histo[-12:]
    ret = Tool['tpl']((base_prompt+histo) + Message('user','{user_input}'), **ctx)
    
    ctx['agent'].append_histo(ret[-1])
    
    return ret
 