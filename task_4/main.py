class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def rate_lecture(self, lecturer, course, grade):
        if isinstance(lecturer, Lecturer) and course in self.courses_in_progress and course in lecturer.courses_attached:
            if course in lecturer.grades:
                lecturer.grades[course].append(grade)
            else:
                lecturer.grades[course] = [grade]
            return
        else:
            return 'Ошибка'

    def get_average_grade(self):
        if not self.grades:
            return 0
        all_grades = []
        for grades_list in self.grades.values():
            all_grades.extend(grades_list)
        if not all_grades:
            return 0
        return sum(all_grades) / len(all_grades)

    def __str__(self):
        avg_grade = self.get_average_grade()
        courses_in_progress_str = ', '.join(self.courses_in_progress)
        finished_courses_str = ', '.join(self.finished_courses)
        res = f"Имя: {self.name}\nФамилия: {self.surname}\n"
        res += f"Средняя оценка за домашние задания: {avg_grade}\n"
        res += f"Курсы в процессе изучения: {courses_in_progress_str}\n"
        res += f"Завершенные курсы: {finished_courses_str}"
        return res

    def __lt__(self, other):
        if isinstance(other, Student):
            return self.get_average_grade() < other.get_average_grade()
        return NotImplemented


class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []

    def __str__(self):
        return f"Имя: {self.name}\nФамилия: {self.surname}"


class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}

    def get_average_grade(self):
        if not self.grades:
            return 0
        total = []
        for grades_list in self.grades.values():
            total.extend(grades_list)
        if not total:
            return 0
        return sum(total) / len(total)

    def __str__(self):
        avg_grade = self.get_average_grade()
        return f"Имя: {self.name}\nФамилия: {self.surname}\nСредняя оценка за лекции: {avg_grade}"

    def __lt__(self, other):
        if isinstance(other, Lecturer):
            return self.get_average_grade() < other.get_average_grade()
        return NotImplemented


class Reviewer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)

    def rate_hw(self, student, course, grade):
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course].append(grade)
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'

    def __str__(self):
        return f"Имя: {self.name}\nФамилия: {self.surname}"


# Создание экземпляров классов
best_student = Student('Анна', 'Смирнова', 'female')
another_student = Student('Дмитрий', 'Волков', 'male')

cool_lecturer = Lecturer('Иван', 'Иванов')
another_lecturer = Lecturer('Мария', 'Петрова')

first_reviewer = Reviewer('Пётр', 'Петров')
second_reviewer = Reviewer('Елена', 'Сидорова')

# Тестируем работу методов
best_student.courses_in_progress.append('Python')
best_student.courses_in_progress.append('Git')
best_student.finished_courses.append('Введение в программирование')

another_student.courses_in_progress.append('Python')
another_student.courses_in_progress.append('Java')

cool_lecturer.courses_attached.append('Python')
cool_lecturer.courses_attached.append('Git')
another_lecturer.courses_attached.append('Python')
another_lecturer.courses_attached.append('Java')

# Оцениваем лекции
best_student.rate_lecture(cool_lecturer, 'Python', 9)
another_student.rate_lecture(cool_lecturer, 'Python', 8)
best_student.rate_lecture(another_lecturer, 'Python', 10)
another_student.rate_lecture(another_lecturer, 'Python', 7)

# Проверяем работу методов
print(best_student)
print()
print(another_student)
print()
print(cool_lecturer)
print()
print(another_lecturer)
print()

# Сравниваем студентов и лекторов
print(f"Лучший ли студент - Анна? {best_student < another_student}")
print(f"У первого лектора оценка лучше? {cool_lecturer < another_lecturer}")
print()


def calc_average_hw_grade(students, course):
    """
    Подсчет средней оценки за домашние задания по всем студентам в рамках конкретного курса
    """
    total_grades = []
    for student in students:
        if course in student.grades:
            total_grades.extend(student.grades[course])
    
    if not total_grades:
        return 0
    
    return sum(total_grades) / len(total_grades)


def calc_average_lecture_grade(lecturers, course):
    """
    Подсчет средней оценки за лекции всех лекторов в рамках курса
    """
    total_grades = []
    for lecturer in lecturers:
        if course in lecturer.grades:
            total_grades.extend(lecturer.grades[course])
    if not total_grades:
        return 0
    return sum(total_grades) / len(total_grades)


# Пример использования функций
students = [best_student, another_student]
lecturers = [cool_lecturer, another_lecturer]

print("Средняя оценка за ДЗ по Python:", calc_average_hw_grade(students, 'Python'))
print("Средняя оценка за лекции по Python:", calc_average_lecture_grade(lecturers, 'Python'))