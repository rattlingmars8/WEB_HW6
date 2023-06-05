SELECT s.fullname AS student_fullname, t.fullname AS teacher_fullname, sub.sub_name AS subject_name
FROM students s
JOIN grades g ON s.id = g.student_id
JOIN subjects sub ON g.subject_id = sub.id
JOIN teachers t ON sub.teacher_id = t.id
WHERE s.fullname = 'Ілля Єрченко' AND t.fullname = 'пан Віталій Овчаренко'
GROUP BY sub.sub_name;
