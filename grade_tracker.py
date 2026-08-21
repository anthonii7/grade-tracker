import csv

def load_students(filepath):
    """Loads student data from CSV and returns a list of dictionaries."""
    students = []
    try:
        with open(filepath, newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                students.append(row)
    except FileNotFoundError:
        print(f"Error: Could not find the file {filepath}")
        return []
    return students

def calculate_average(grades):
    """Calculates the average of a list of grades, ADDED ignoring empty strings."""
    valid_grades = []
    for grade in grades:
        if grade != '':
            valid_grades.append(float(grade)) # coverts to float since csv = strings
    if len(valid_grades) == 0:
        return None
    total = 0
    for grade in valid_grades:
        total = total + grade
    return round(total / len(valid_grades), 1) # rounds to 1 decimal place

def get_letter_grade(average):
    """Returns the letter grade corresponding to the average."""
    if average is None:
        return "N/A"
    elif average >= 90:
        return "A"
    elif average >= 80:
        return "B"
    elif average >= 70:
        return "C"
    elif average >= 60:
        return "D"
    else:
        return "F"

def generate_report(students):
    """Generates a report dictionary containing class statistics and student results."""
    grade_distribution = {"A": 0, "B": 0, "C": 0, "D": 0, "F": 0, "N/A": 0}
    student_results = []

    for student in students:
        name = student['student_name']
        grades = [student['math'], student['science'], student['english'], student['history']]
        average = calculate_average(grades)
        letter = get_letter_grade(average)
        grade_distribution[letter] = grade_distribution[letter] + 1
        student_results.append({'name': name, 'average': average, 'letter_grade': letter})

    valid_averages = []
    for s in student_results:
        if s['average'] is not None:
            valid_averages.append(s['average'])

    total = 0
    for avg in valid_averages:
        total = total + avg

    if len(valid_averages) == 0:
        class_average = None
    else:
        class_average = round(total / len(valid_averages), 1)

    if len(valid_averages) == 0:
        highest = None
        lowest = None
    else:
        highest = valid_averages[0]
        lowest = valid_averages[0]
        for avg in valid_averages:
            if avg > highest:
                highest = avg
            if avg < lowest:
                lowest = avg

    top_students = []
    for s in student_results:
        top_students.append(s)
    top_students_sorted = []
    remaining = top_students
    for i in range(min(5, len(remaining))):
        best = remaining[0]
        for s in remaining:
            if (s['average'] or 0) > (best['average'] or 0):
                best = s
        top_students_sorted.append(best)
        remaining = [s for s in remaining if s != best]

    return {
        'total_students': len(students),
        'class_average': class_average,
        'highest_average': highest,
        'lowest_average': lowest,
        'grade_distribution': grade_distribution,
        'top_students': top_students_sorted,
        'all_students': student_results
    }
def write_report(report, filepath):
    """Writes the report to a text file."""
    with open(filepath, 'w') as f: # w here is the key to overwrite the file each time, otherwise it would add
        f.write("--- Summary ---\n")
        f.write(f"Total students:   {report['total_students']}\n")
        f.write(f"Class average:    {report['class_average']}\n")
        f.write(f"Highest average:  {report['highest_average']}\n")
        f.write(f"Lowest average:   {report['lowest_average']}\n")

        f.write("\nGrade Distribution:\n")
        for grade, count in report['grade_distribution'].items():
            f.write(f"  {grade}: {count}\n")

        f.write("\nTop 5 students:\n")
        for s in report['top_students']:
            f.write(f"  {s['name']:<20} {s['average']}  ({s['letter_grade']})\n")

def main():
    print("Loading student data...")
    students = load_students("data/students.csv")
    print(f"  Loaded {len(students)} students.")

    print("\nGenerating report...")
    report = generate_report(students)

    print("\n--- Summary ---")
    print(f"Total students:   {report['total_students']}")
    print(f"Class average:    {report['class_average']}")
    print(f"Highest average:  {report['highest_average']}")
    print(f"Lowest average:   {report['lowest_average']}")

    print("\nGrade Distribution:")
    for grade, count in report['grade_distribution'].items():
        print(f"  {grade}: {count}")

    print("\nTop 5 students:")
    for s in report['top_students']:
        print(f"  {s['name']:<20} {s['average']}  ({s['letter_grade']})")

    write_report(report, "grade_report.txt")
    print("\nReport written to grade_report.txt")

main()
