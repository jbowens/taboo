select a.wid, a.word, a.status, b.wid, b.status
from words AS a
INNER JOIN words AS b
ON lower(a.word) = b.word AND a.wid != b.wid;
