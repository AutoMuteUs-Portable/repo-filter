from rich.progress import Progress, TaskID


class GitProgressHandler:
    def __init__(self, progress: Progress, task: TaskID):
        self.progress = progress
        self.task = task

    def __call__(self, op_code, cur_count, max_count=None, message=""):
        if max_count != None:
            self.progress.update(self.task, completed=cur_count, total=max_count)
