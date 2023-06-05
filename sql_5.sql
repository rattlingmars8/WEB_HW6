select distinct sub.sub_name, teachers.fullname
from subjects sub
join teachers on sub.teacher_id = teachers.id
where teachers.fullname = "пан Віталій Овчаренко"
