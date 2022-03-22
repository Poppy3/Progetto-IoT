"""DEVELOPMENT ONLY"""

from ..extensions import scheduler


@scheduler.task(
    "interval",
    id="job_sync",
    seconds=10,
    max_instances=1,
    start_date="2000-01-01 12:19:00",
)
def task1():
    """Sample task 1.
    Added when app starts.
    """
    print("running task 1!")  # noqa: T001

    # oh, do you need something from config?
    with scheduler.app.app_context():
        # print(scheduler.app.config)
        pass
