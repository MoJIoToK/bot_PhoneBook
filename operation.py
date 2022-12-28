import logger 
import csv

def Create(name='', surname='', number='', description=''):

    book = []

    book.append(name.title())
    book.append(surname.title())
    book.append(number)
    book.append(description)

    with open('Book.csv', 'a', encoding='utf-8-sig') as book_csv:
        book_csv.write('{};{};{};{}\n'
                    .format(book[0], book[1], book[2], book[3]))

    return book


def Print_csv():
    with open('Book.csv', 'r', encoding='utf-8-sig') as book_csv:
        result = book_csv.read()
        return result


def Import_txt(filename):
        with open(f'{filename}', 'r', encoding='utf-8-sig') as file:
            str1 = file.read()
            r = str1.replace('\n', ';')
            z = r.replace(';;', '\n')
            a = list(z.split('\n'))
            with open('Book.csv', 'a', encoding='utf-8-sig') as file:
                for i in range(0, len(a)):
                    file.write(f'{a[i]}\n')


def Import_csv(filename):
        with open(filename, 'r', encoding='utf-8-sig') as file:
            data = file.read()
            with open('Book.csv', 'a', encoding='utf-8-sig') as file:
                file.write(data)


def print_log():
    with open('log.csv', 'r') as file:
        result = file.read()
        return result


def Export_csv(filename):  
        with open('Book.csv', 'r', encoding='utf-8-sig') as file:
            reader = csv.reader(file, delimiter=';')
            with open(filename, 'w', encoding='utf-8-sig', newline='') as file:
                writer = csv.writer(file, delimiter=';')
                for row in reader:
                    writer.writerow(row)


def Export_txt(filename):  
        with open('Book.csv', 'r', encoding='utf-8-sig') as file:
            reader = csv.reader(file, delimiter=';')
            with open(filename, 'w', encoding='utf-8-sig') as file:
                writer = csv.writer(file, delimiter='\n')
                for i, row in enumerate(reader):
                    writer.writerow(row)