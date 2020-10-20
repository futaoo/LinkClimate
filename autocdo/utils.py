import datetime

def split_date_by_month(begin, end):

    dt_start = datetime.datetime.strptime(begin, '%Y-%m-%d')
    dt_end = datetime.datetime.strptime(end, '%Y-%m-%d')
    one_day = datetime.timedelta(1)
    start_dates = [dt_start]
    end_dates = []
    today = dt_start
    while today < dt_end:
        #print(today)
        tomorrow = today + one_day
        if tomorrow.month != today.month:
            start_dates.append(tomorrow)
            end_dates.append(today)
        today = tomorrow
    end_dates.append(dt_end)
    out_fmt = '%Y-%m-%d'
    time_intervals = []
    for start, end in zip(start_dates,end_dates):
        time_intervals.append({'startdate':start.strftime(out_fmt), 'enddate': end.strftime(out_fmt)})
        
    return time_intervals

def a_week_before(date_of_today):
    out_fmt = '%Y-%m-%d'
    date_of_today = datetime.datetime.today()
    one_week = datetime.timedelta(6)
    date_before_a_week = date_of_today-one_week
    return date_before_a_week.strftime(out_fmt)

