select sub.sub_name, s.fullname, round(AVG(g.grade), 2) as average_grade
from grades g
join students s on s.id = g.student_id
join subjects sub on sub.id = g.subject_id
where sub.id = 5
group by s.fullname
order by  average_grade DESC
limit 1