from datetime import timedelta


def calc_diff_start(date):
    # 月曜日を最初とした場合の、週1日目との差を生成
    # ex)2000/01/01は土曜日 == 週の初めの12/27との差は6
    return date.weekday()


def calc_diff_end(date):
    # 月曜日を最初とした場合の、週7日目との差を生成
    return 6 - date.weekday()


def fill_nums(nums, start, end):
    return [None for _ in range(calc_diff_start(start))] + nums + [None for _ in range(calc_diff_end(end))]


def gen_weekly_num_lists(patient_records):
    """月曜日を週の初めとした場合の、1週間毎に区切った日毎の感染者数を生成。

    Parameters
    ----------
    patient_records: list[PatientsModel]

    Returns
    -------
    list[list[int]]"""
    nums = [row.num for row in patient_records]

    filled_nums = fill_nums(
        nums,
        patient_records[0].publication_date,
        patient_records[len(patient_records) - 1].publication_date
    )

    # 1週間 == 7日
    one_week = 7
    # 週の数
    week_num = int(len(filled_nums) / one_week)

    weekly_num_lists = []

    for idx in range(week_num):
        start = idx * one_week
        stop = start + one_week
        weekly_num_lists.append(filled_nums[start:stop])

    return weekly_num_lists


def gen_header_dates(start, end, fmt="%m/%d"):
    """見出しの日付を生成.

    Parameters
    ----------
    start: date
    end: date
    fmt: str
        日付フォーマット

    Returns
    -------
    list[str]"""
    start = start - timedelta(days=calc_diff_start(start))
    end = end + timedelta(days=calc_diff_end(end))
    diff = (end - start).days

    return [(start + timedelta(days=num)).strftime(fmt)
            for num in range(0, diff, 7)]


def gen_weekly_totals(weekly_num_lists):
    """週毎の合計値を計算.

    Parameters
    ----------
    weekly_num_lists: list[list[int]]

    Returns
    -------
    list[int]"""
    totals = []
    for nums in weekly_num_lists:
        totals.append(sum([int(num_or_none or 0) for num_or_none in nums]))

    return totals
