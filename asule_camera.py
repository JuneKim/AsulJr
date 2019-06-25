
def runCamera(tasks):
	while True:
		tasks.put_nowait("ABCD")

	tasks.task_done()