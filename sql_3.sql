select sub.sub_name, gr.name, round(AVG(g.grade), 2) as average_grade
from grades g
join students s on s.id = g.student_id
join subjects sub on sub.id = g.subject_id
join groups gr on gr.id = s.group_id
where sub.id = 2
group by gr.name
order by  average_grade DESC