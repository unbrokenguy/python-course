def views_count_by_date_for_object(model):
    views = model.views.all()
    views_count_by_date = {}

    for view in views:
        if str(view.date) not in views_count_by_date.keys():
            views_count_by_date[str(view.date)] = 0
        views_count_by_date[str(view.date)] += 1

    return views_count_by_date
