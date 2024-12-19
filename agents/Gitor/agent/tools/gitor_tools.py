from agentix import tool, State



@tool
def gitor_current_repo():
    if not 'Gitor' in State:
        State['Gitor'] = {
            "current_repo":"no_repo_yet",
            "repos":{}
        }
    return State['Gitor']['current_repo']

@tool
def gitor_pwd():
    return 'tatayoyo'

@tool
def gitor_last_reported_commit():
    current_repo = State['Gitor'].current_repo
    if not current_repo in State['Gitor']['repos']:
        return "no_commit_yet"
    return State['Gitor']['repos'][current_repo].last_commit

@tool
def report_git_change(diff, repo, commit_id):
    """
    Reports a git change by updating the state with the new commit information and diff
    
    Args:
        diff (str): The diff content of the commit
        repo (str): The repository name
        commit_id (str): The commit identifier
    """
    if not 'Gitor' in State:
        State['Gitor'] = {
            "current_repo": "no_repo_yet",
            "repos": {}
        }
    
    if not repo in State['Gitor']['repos']:
        State['Gitor']['repos'][repo] = {
            "last_commit": "no_commit_yet",
            "diffs": {

            }
        }
    import time
    State['Gitor']['repos'][repo]['last_commit'] = commit_id
    State['Gitor']['repos'][repo]['diffs'][commit_id] = {
        "timestamp": int(time.time()),
        "handled": False,
        "commit_id": commit_id,
        "diff": diff
    }
    State['Gitor']['current_repo'] = repo
    
    return "Reported :)"