# ניהול ספרייה — Library API

## מטרת התוכנית
ניהול ספרייה ואת החברים בה בכל מה שנוגע בהשאלת ספרים, ניהול ספרים וניהול חברים בספרייה — רץ מול מסד נתונים.

---

## הרצת Docker

```bash
docker run --name mysql-9 \
  -e MYSQL_ROOT_PASSWORD=root \
  -e MYSQL_DATABASE=library_db \
  -p 3306:3306 \
  -d mysql:latest
```

---

## מבנה התיקיות

```
library-api/
│
├── app/
│   ├── main.py
│   ├── database/
│   │   ├── db_connection.py
│   │   ├── book_db.py
│   │   └── member_db.py
│   ├── routes/
│   │   ├── book_routes.py
│   │   ├── member_routes.py
│   │   └── report_routes.py
│   └── logs/
│       └── app.log
│
├── README.md
├── requirements.txt
└── .gitignore
```

---

## מבנה הטבלאות

### טבלת `books`

| שדה | הסבר |
|-----|-------|
| `id` | מפתח ראשי |
| `title` | כותרת הספר, עמודה לא ריקה, מקסימום 50 תווים |
| `author` | שם המחבר, עמודה לא ריקה, מקסימום 50 תווים |
| `genre` | ערכי genre מותרים: Fiction |
| `is_available` | האם הספר זמין להשאלה — `FALSE` מסמן הושאל, עמודה לא ריקה |
| `borrowed_by_member_id` | מזהה החבר שמחזיק את הספר — `NULL` אם זמין |

### טבלת `members`

| שדה | הסבר |
|-----|-------|
| `id` | מפתח ראשי |
| `name` | שם החבר, עמודה לא ריקה, מקסימום 50 תווים |
| `email` | כתובת מייל — ייחודית, עמודה לא ריקה |
| `is_active` | האם החבר פעיל — `FALSE` לא יכול להשאיל, עמודה לא ריקה |
| `total_borrows` | מונה סה"כ השאלות — עולה ב-1 בכל השאלה, עמודה לא ריקה |

---

## חוקי מערכת

| חוק | נושא | הכלל |
|-----|-------|-------|
| 1 | יצירת ספר | המשתמש שולח `title`/`author`/`genre` — המערכת מוסיפה `is_available=True`, `borrowed_by=NULL` |
| 2 | genre | חייב להיות `Fiction` / `Non-Fiction` / `Science` / `History` / `Other` — כל ערך אחר מחזיר שגיאה. יש לוודא הן בהוספה (`POST`) והן בעדכון (`PATCH`) |
| 3 | יצירת חבר | המשתמש שולח `name`/`email` — המערכת מוסיפה `is_active=True`, `total_borrows=0` |
| 4 | email | חייב להיות ייחודי — אם קיים כבר מחזיר שגיאה |
| 5 | חבר לא פעיל | אם `is_active=False` — אי אפשר להשאיל ספר |
| 6 | ספר לא זמין | אי אפשר להשאיל ספר שכבר מושאל (`is_available=False`) |
| 7 | מקסימום ספרים | חבר לא יכול להחזיק יותר מ-3 ספרים בו-זמנית |
| 8 | החזרת ספר | ניתן להחזיר ספר רק אם הוא מושאל לאותו חבר שמחזיר אותו |

---

## Logging

**פורמט חובה:**
```
time | level | message
```

**חובה לכתוב לוג:**
- בתחילת כל REST
- לפני עדכונים מול SQL
- במקרה של שגיאה
- בסיום כל REST

---

## Endpoints

### Books

| Method | Endpoint | תיאור |
|--------|----------|-------|
| `POST` | `/books` | יצירת ספר |
| `GET` | `/books` | כל הספרים |
| `GET` | `/books/{id}` | ספר לפי ID |
| `PATCH` | `/books/{id}` | עדכון ספר |
| `PATCH` | `/books/{id}/borrow/{member_id}` | השאלת ספר לחבר |
| `PATCH` | `/books/{id}/return/{member_id}` | החזרת ספר מחבר |

### Members

| Method | Endpoint | תיאור |
|--------|----------|-------|
| `POST` | `/members` | יצירת חבר |
| `GET` | `/members` | כל החברים |
| `GET` | `/members/{id}` | חבר לפי ID |
| `PATCH` | `/members/{id}` | עדכון חבר |
| `PATCH` | `/members/{id}/deactivate` | השבתת חבר |
| `PATCH` | `/members/{id}/activate` | הפעלת חבר |

### Reports

| Method | Endpoint | תיאור |
|--------|----------|-------|
| `GET` | `/reports/summary` | דוח כללי |
| `GET` | `/reports/books-by-genre` | ספרים לפי ז'אנר |
| `GET` | `/reports/top-member` | החבר הכי פעיל |

---

## זרימת המערכת

```
Http Requests → FastAPI → Endpoint → DAL → Database
```
