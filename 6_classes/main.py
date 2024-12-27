class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def __str__(self):
        delimiter = '\n'
        out_str = (f'Имя: {self.name}{delimiter}Фамилия: '
                   f'{self.surname}{delimiter}'
                   f'Средняя оценка за домашние задания: '
                   f'{self.avr_grade()}{delimiter}'
                   f'Курсы в процессе изучения: '
                   f'{", ".join(self.courses_in_progress)}{delimiter}' 
                   f'Завершенные курсы: {", ".join(self.finished_courses)}'
                   f'{delimiter}')
        return out_str

    def __eq__(self, other):
        return self.avr_grade() == other.avr_grade()

    def __lt__(self, other):
        return self.avr_grade() < other.avr_grade()

    def __le__(self, other):
        return self.avr_grade() <= other.avr_grade()

    def avr_grade(self):
        # Расчет средней оценки за домашние задания по всем курсам
        grades_total = [grade for grades in self.grades.values()
                        for grade in grades]
        return round(avr_calc(grades_total), 1)

    def rate_lectures(self, lecturer, course, grade):
        # Выставление студентом оценки лектору за лекцию
        # Студент может выставить оценку из диапазона 1-10
        legal_grades = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
        if grade not in legal_grades:
            raise ValueError(f"Оценка {grade} не в диапазоне от 1 до 10.")
        # Студент может выставить оценку лектору, закрепленному за курсом,
        # который студент изучает или уже окончил
        if not isinstance(lecturer, Lecturer):
            raise ValueError("Ожидается объект класса Lecturer.")

        if course not in lecturer.courses_attached:
            raise ValueError(f"Лектор {lecturer.surname} "
                             f"не ведет курс '{course}'")

        if not course in self.courses_in_progress + self.finished_courses:
            raise ValueError(f"Курс '{course}' "
                             f"не найден у студента {self.surname}")

        lecturer.grades.setdefault(course, []).append(grade)


class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []


class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}

    def __str__(self):
        delimiter = '\n'
        out_str = (f'Имя: {self.name}{delimiter}Фамилия: '
                   f'{self.surname}{delimiter}'
                   f'Средняя оценка за лекции: {self.avr_grade()}{delimiter}')
        return out_str

    def avr_grade(self):
        # Расчет средней оценки за лекции по всем курсам, которые читает лектор
        grades_total = [grade for grades in self.grades.values()
                        for grade in grades]
        return round(avr_calc(grades_total), 1)

    def __eq__(self, other):
        return self.avr_grade() == other.avr_grade()

    def __lt__(self, other):
        return self.avr_grade() < other.avr_grade()

    def __le__(self, other):
        return self.avr_grade() <= other.avr_grade()


class Reviewer(Mentor):
    def rate_hw(self, student, course, grade):
        # Выставление проверяющим оценки студенту по курсу
        legal_grades = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
        if grade not in legal_grades:
            raise ValueError(f"Оценка {grade} не в диапазоне от 1 до 10.")

        if not isinstance(student, Student):
            raise ValueError("Ожидается объект класса Student.")

        if course not in self.courses_attached:
            raise ValueError(f"Лектор {self.surname} не ведет курс '{course}'")

        if course not in student.courses_in_progress:
            raise ValueError((f"Студент {student.surname} "
                              f"не изучает курс '{course}'"))

        student.grades.setdefault(course, []).append(grade)

    def __str__(self):
        delimiter = '\n'
        out_str = (f'Имя: {self.name}{delimiter}'
                   f'Фамилия: {self.surname}{delimiter}')
        return out_str


def avr_calc(grades):
    return sum(grades) / len(grades) if grades else 0


def avr_grade(person_lst, course_name):
    # Расчет средней оценки по курсу, по всем студентам,
    # изучающим курс, или лекторам, читающим курс
    avr_grades = []
    for person in person_lst:
        if course_name in person.grades:
            grades_sum = sum(person.grades[course_name])
            grades_num = len(person.grades[course_name])
            avr_grades.append(grades_sum / grades_num)
    return round(sum(avr_grades) / len(avr_grades), 1)


# Задание №1

student_1 = Student('Иван', 'Петров', 'male')
student_1.courses_in_progress += ['Python']
student_1.courses_in_progress += ['Git']
student_1.finished_courses += ['Введение в программирование']

student_2 = Student('Анна', 'Кузнецова', 'female')
student_2.courses_in_progress += ['Python']
student_2.courses_in_progress += ['Git']
student_2.finished_courses += ['Введение в программирование']

reviewer_1 = Reviewer('Пётр', 'Васильев')
reviewer_1.courses_attached += ['Python']
reviewer_2 = Reviewer('Александр', 'Бессонов')
reviewer_2.courses_attached += ['Git']

lecturer_1 = Lecturer('Алексей', 'Воронов')
lecturer_1.courses_attached += ['Python']
lecturer_2 = Lecturer('Илья', 'Соколов')
lecturer_2.courses_attached += ['Git']
lecturer_2.courses_attached += ['Python']

# Задание №2

reviewer_1.rate_hw(student_1, 'Python', 10)
reviewer_1.rate_hw(student_1, 'Python', 8)
reviewer_1.rate_hw(student_1, 'Python', 7)

reviewer_1.rate_hw(student_2, 'Python', 9)
reviewer_1.rate_hw(student_2, 'Python', 10)
reviewer_1.rate_hw(student_2, 'Python', 10)

reviewer_2.rate_hw(student_1, 'Git', 7)
reviewer_2.rate_hw(student_1, 'Git', 8)
reviewer_2.rate_hw(student_1, 'Git', 9)

reviewer_2.rate_hw(student_2, 'Git', 9)
reviewer_2.rate_hw(student_2, 'Git', 9)
reviewer_2.rate_hw(student_2, 'Git', 10)

student_1.rate_lectures(lecturer_1, 'Python', 8)
student_1.rate_lectures(lecturer_1, 'Python', 9)
student_1.rate_lectures(lecturer_1, 'Python', 8)
student_1.rate_lectures(lecturer_2, 'Git', 9)
student_1.rate_lectures(lecturer_2, 'Git', 9)
student_1.rate_lectures(lecturer_2, 'Python', 10)

student_2.rate_lectures(lecturer_1, 'Python', 10)
student_2.rate_lectures(lecturer_1, 'Python', 9)
student_2.rate_lectures(lecturer_1, 'Python', 10)
student_2.rate_lectures(lecturer_2, 'Git', 7)
student_2.rate_lectures(lecturer_2, 'Git', 8)
student_2.rate_lectures(lecturer_2, 'Python', 10)

# Задание №3.1: Перегрузить магический метод __str__ у всех классов

print('\nСтуденты:')
print(student_1)
print(student_2)

print('\nПроверяющие:')
print(reviewer_1)
print(reviewer_2)

print('\nЛекторы:')
print(lecturer_1)
print(lecturer_2)

# Задание №3.2: Реализуйте возможность сравнивать (через операторы сравнения)
# между собой лекторов по средней оценке за лекции
# и студентов по средней оценке за домашние задания.

print('\nСравнение студентов:')
print(f'{student_1.surname} == {student_2.surname}: {student_1 == student_2}')
print(f'{student_1.surname} < {student_2.surname}: {student_1 < student_2}')
print(f'{student_1.surname} <= {student_2.surname}: {student_1 <= student_2}')
print(f'{student_1.surname} > {student_2.surname}: {student_1 > student_2}')
print(f'{student_1.surname} >= {student_2.surname}: {student_1 >= student_2}')
print('\nСравнение лекторов:')
print((f'{lecturer_1.surname} == {lecturer_2.surname}, '
       f'{lecturer_1 == lecturer_2}'))
print((f'{lecturer_1.surname} < {lecturer_2.surname}, '
       f'{lecturer_1 < lecturer_2}'))
print((f'{lecturer_1.surname} <= {lecturer_2.surname}, '
       f'{lecturer_1 <= lecturer_2}'))
print((f'{lecturer_1.surname} > {lecturer_2.surname}, '
       f'{lecturer_1 > lecturer_2}'))
print((f'{lecturer_1.surname} >= {lecturer_2.surname}, '
       f'{lecturer_1 >= lecturer_2}'))

# Задание №4: Реализуйте две функции:
# 1. для подсчета средней оценки за домашние задания по всем студентам в
# рамках конкретного курса (в качестве аргументов принимаем список студентов
# и название курса);
# 2. для подсчета средней оценки за лекции всех лекторов в рамках курса
# (в качестве аргумента принимаем список лекторов и название курса).
#
# Так как расчет средней оценки как студентов так и лекторов одинаков,
# он реализован одной функцией avr_grade()

students_list = [student_1, student_2]
course_f = 'Git'
print((f'\nСредняя оценка студентов за домашние задания по курсу {course_f}: '
       f'{avr_grade(students_list, course_f)}'))

lecturers_list = [lecturer_1, lecturer_2]
course_f = 'Python'
print((f'\nСредняя оценка лекторов за лекции по курсу {course_f}: '
       f'{avr_grade(lecturers_list, course_f)}'))

student_3 = Student('No', 'One', '')
print()
print(student_3)
lecturer_3 = Lecturer('Un', 'Known')
print(lecturer_3)

try:
    reviewer_1.rate_hw(student_3, 'Python', 10)
except Exception as e:
    print(e)
try:
    reviewer_1.rate_hw(student_1, 'Art', 10)
except Exception as e:
    print(e)
try:
    reviewer_1.rate_hw(student_1, 'Python', 'Bad')
except Exception as e:
    print(e)
try:
    reviewer_1.rate_hw(student_1, 'Git', 10)
except Exception as e:
    print(e)

try:
    student_3.rate_lectures(lecturer_1, 'Python', 10)
except Exception as e:
    print(e)
try:
    student_1.rate_lectures(lecturer_1, 'Git', 10)
except Exception as e:
    print(e)
