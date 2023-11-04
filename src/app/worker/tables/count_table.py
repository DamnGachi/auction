from src.app.worker.init import get_faust_app

faust_app = get_faust_app()

count_table = faust_app.GlobalTable(
    "count",
    default=int,
    partitions=1,
)
