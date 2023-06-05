select s.fullname, sub.sub_name, gr.name, g.grade
from students s
join grades g on s.id = g.student_id
join subjects sub on g.subject_id = sub.id
join groups gr on s.group_id = gr.id
where gr.name = "Group 3"
and sub.id = "8"