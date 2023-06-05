select s.fullname, gr.name
from students s
join groups gr on gr.id = s.group_id
where gr.name == "Group 3"
