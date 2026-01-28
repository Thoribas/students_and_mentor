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
        all_grades = []
        for grades_list in self.grades.values():
            all_grades.extend(grades_list)
        if not all_grades:
            return 0
        return sum(all_grades) / len(all_grades)

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


# Тестируем работу методов
some_reviewer = Reviewer('Some', 'Buddy')
print(some_reviewer)
print()

some_lecturer = Lecturer('Some', 'Buddy')
some_lecturer.grades = {'Python': [10, 9, 10, 10]}  # Добавляем оценки для тестирования
print(some_lecturer)
print()

some_student = Student('Ruoy', 'Eman', 'your_gender')
some_student.courses_in_progress = ['Python', 'Git']
some_student.finished_courses = ['Введение в программирование']
some_student.grades = {'Python': [10, 9, 10, 10]}  # Добавляем оценки для тестирования
print(some_student)
print()

# Проверяем сравнения
print("Сравнение лекторов:")
lecturer1 = Lecturer('Иван', 'Иванов')
lecturer2 = Lecturer('Мария', 'Петрова')
lecturer1.grades = {'Python': [8, 9, 10]}
lecturer2.grades = {'Python': [7, 8, 9]}
print(f"lecturer1 > lecturer2: {lecturer1 > lecturer2}")

print("\nСравнение студентов:")
student1 = Student('Анна', 'Смирнова', 'female')
student2 = Student('Дмитрий', 'Волков', 'male')
student1.grades = {'Python': [9, 10, 8]}
student2.grades = {'Python': [7, 8, 9]}
print(f"student1 > student2: {student1 > student2}")

# Тестирование метода оценки лекций
lecturer = Lecturer('Иван', 'Иванов')
reviewer = Reviewer('Пётр', 'Петров')
student = Student('Алёхина', 'Ольга', 'Ж')

student.courses_in_progress += ['Python', 'Java']
lecturer.courses_attached += ['Python', 'C++']
reviewer.courses_attached += ['Python', 'C++']

print(student.rate_lecture(lecturer, 'Python', 7))   # None
print(student.rate_lecture(lecturer, 'Java', 8))     # Ошибка
print(student.rate_lecture(lecturer, 'C++', 8))      # Ошибка
print(student.rate_lecture(reviewer, 'Python', 6))   # Ошибка

print(lecturer.grades)  # {'Python': [7]}