SELECT t.id AS teacher_id, t.fullname AS teacher_fullname, sub.sub_name, ROUND(AVG(g.grade)) AS average_grade
FROM grades g
JOIN subjects sub ON g.subject_id = sub.id
JOIN teachers t ON sub.teacher_id = t.id
JOIN students s ON g.student_id = s.id
WHERE t.fullname = 'пан Віталій Овчаренко'
GROUP BY t.id, t.fullname, sub.sub_name;
