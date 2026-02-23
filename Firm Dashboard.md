# Firm Dashboard

## Today's Action Items

> [!todo] Unblocked Landmarks
> ```dataview
> TABLE WITHOUT ID
>   file.link as "Case",
>   client_name as "Client",
>   current_phase as "Phase"
> FROM "cases"
> WHERE current_phase != "closed"
>   AND landmarks
> FLATTEN landmarks as landmark
> WHERE landmark.status = "unblocked"
> SORT sol_deadline ASC
> LIMIT 20
> ```

> [!check] Pending Tasks
> ```dataview
> TABLE WITHOUT ID
>   file.link as "Case",
>   client_name as "Client",
>   task_name as "Task",
>   due_date as "Due"
> FROM "cases"
> WHERE tasks
> FLATTEN tasks as task
> WHERE task.status = "pending"
>   AND task.due_date <= date(today) + dur(7 days)
> SORT task.due_date ASC
> LIMIT 15
> ```

> [!warning]- SOL Critical (< 90 days)
> ```dataview
> TABLE WITHOUT ID
>   file.link as "Case",
>   client_name as "Client",
>   date_of_incident as "DOI",
>   sol_deadline as "SOL Deadline",
>   round((sol_deadline - date(today)).days) as "Days Left",
>   current_phase as "Phase"
> FROM "cases"
> WHERE sol_deadline
>   AND current_phase != "closed"
>   AND round((sol_deadline - date(today)).days) < 90
>   AND round((sol_deadline - date(today)).days) > 0
> SORT sol_deadline ASC
> ```

> [!abstract]- Cases by Phase
> ```dataview
> TABLE WITHOUT ID
>   current_phase as "Phase",
>   length(rows) as "Count",
>   join(map(rows, (r) => "[[" + r.file.path + "|" + r.client_name + "]]"), ", ") as "Cases"
> FROM "cases"
> WHERE current_phase AND current_phase != "closed"
> GROUP BY current_phase
> SORT length(rows) DESC
> ```

> [!warning]- Stale Cases (no activity in 30+ days)
> ```dataview
> TABLE WITHOUT ID
>   file.link as "Case",
>   client_name as "Client",
>   current_phase as "Phase",
>   last_activity as "Last Activity",
>   round((date(today) - last_activity).days) as "Days Stale"
> FROM "cases"
> WHERE current_phase != "closed"
>   AND last_activity
>   AND round((date(today) - last_activity).days) > 30
> SORT (date(today) - last_activity) DESC
> ```

> [!calendar]- Upcoming Deadlines (next 30 days)
> ```dataview
> TABLE WITHOUT ID
>   file.link as "Case",
>   client_name as "Client",
>   deadline_date as "Deadline",
>   deadline_type as "Type",
>   round((deadline_date - date(today)).days) as "Days Away"
> FROM "cases"
> WHERE deadlines
> FLATTEN deadlines as deadline
> WHERE deadline.date >= date(today)
>   AND deadline.date <= date(today) + dur(30 days)
> SORT deadline.date ASC
> ```
