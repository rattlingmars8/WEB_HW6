SELECT s.id, s.fullname AS student_fullname, sub.sub_name AS subject_name
FROM students s
JOIN grades g ON s.id = g.student_id
JOIN subjects sub ON g.subject_id = sub.id
WHERE s.fullname = "Ілля Єрченко"
group by sub.sub_name
