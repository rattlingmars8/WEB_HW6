select s.fullname, round(AVG(grade), 2) as average_grade
from grades g
left join students s on s.id = g.student_id
group by s.fullname
order by average_grade DESC
limit 5