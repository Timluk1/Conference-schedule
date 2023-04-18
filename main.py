import datetime as dt

data = {}
ends = {}


class Report:
    def __init__(self, name, conference, start, end):
        year_start, mouth_start, day_start, hour_start, minutes_start = map(int, start.split(":"))
        year_end, mouth_end, day_end, hour_end, minutes_end = map(int, end.split(":"))
        self.conference = conference
        self.time_start = dt.datetime(year_start, mouth_start, day_start, hour_start, minutes_start)
        self.time_end = dt.datetime(year_end, mouth_end, day_end, hour_end, minutes_end)
        self.name = name
        data[conference].append(self)

    def check_report_overlap(self, new_report):
        return (self.time_start <= new_report.time_start <= self.time_end) or \
               (self.time_start <= new_report.time_end <= self.time_end) or \
               (new_report.time_start <= self.time_start <= new_report.time_end) or \
               (new_report.time_start <= self.time_end <= new_report.time_end)

    def check_report_overlap2(self, new_report):
        return (self.conference.start <= new_report.time_start <= self.conference.end) or \
               (self.conference.start <= new_report.time_end <= self.conference.end) or \
               (new_report.time_start <= self.conference.start <= new_report.time_end) or \
               (new_report.time_start <= self.conference.end <= new_report.time_end)

    def time(self):
        return self.time_end - self.time_start


class Conference:
    def __init__(self, name, start, end, topic):
        global data
        year_start, mouth_start, day_start, hour_start, minutes_start = map(int, start.split(":"))
        year_end, mouth_end, day_end, hour_end, minutes_end = map(int, end.split(":"))
        self.name = name
        self.start = dt.datetime(year_start, mouth_start, day_start, hour_start, minutes_start)
        self.end = dt.datetime(year_end, mouth_end, day_end, hour_end, minutes_end)
        self.topic = topic
        data[self] = []

    def time_conference(self):
        return self.end - self.start

    def active_confernces(self):
        print(
            f"Название: {self.name}\nТема: {self.topic}\nНачало: {self.start}\nКонец: {self.end}")

    def time(self):
        return self.end - self.start

    def max_break(self):
        global data
        data2 = sorted(data[self], key=lambda x: x.time_end)
        return max([data2[i + 1].time_start - data2[i].time_end for i in range(len(data2) - 1)])


def delete_end_conferences():
    global data, ends
    dt_now = dt.datetime.now()
    new = {}
    for i in data:
        if i.end > dt_now:
            new[i] = data[i]
        else:
            ends[i] = data[i]

    data = new


def main():
    '''Функция для админа'''
    while True:
        print("Здравствуйте, вы можете создать конференцию и загрузить доклады по конференции.")
        print(
            "Команды:\nВывезти прошедшие конференции\nВывезти идущие конференции\nДобавить конференцию\nДобавить доклад"
            " в конференцию\nВремя самого продолжительного перерыва между докладами\nВыйти")
        answer = input("Введите команду: ")
        if "добавить конференцию" in answer.lower():
            name_conference = input("Введите название концереции: ")
            topic_conference = input("Введите тему концеренции")
            start = input(
                "Введите дату начала конференции, пример: 2024:12:02:10:01, формат (год, месяц, день, часы, минуты: ")
            end = input(
                "Введите дату окончания конференции, пример: 2024:12:02:10:01, формат (год, месяц, день, часы, минуты: ")
            conf = Conference(name_conference, start, end, topic_conference)
            print("Конференция добавлена!")
        elif "вывезти идущие конференции" in answer.lower():
            delete_end_conferences()
            if data == {}:
                print()
                print("Нет идущих конференций")
                print()
            else:
                for i in data:
                    print()
                    i.active_confernces()
                print()
        elif "вывезти прошедшие конференции" in answer.lower():
            delete_end_conferences()
            if ends == {}:
                print()
                print("Нет прошедших конференций")
                print()
            else:
                for i in ends:
                    print()
                    i.active_confernces()
                print()
        elif "добавить доклад в конференцию" in answer.lower():
            print("Доступные конференции: ")
            for i in data:
                print()
                i.active_confernces()
            print()
            name = input("Введите название конференции: ")
            flag = False
            c = ""
            for i in data:
                if i.name == name:
                    c = i
                    flag = True
                    break
            if flag:
                start = input(
                    "Введите дату начала доклада, пример: 2024:12:02:10:01, формат (год, месяц, день, часы, минуты: ")
                end = input(
                    "Введите дату окончания доклада, пример: 2024:12:02:10:01, формат (год, месяц, день, часы, минуты: ")
                name = input("Введите название доклада: ")
                re = Report(name, c, start, end)
                count = 0
                flag = True
                for i in data[c]:
                    if i != re:
                        if re.check_report_overlap(i):
                            print(f"Дата перекрывает уже существуюущую дату {i.time_start, i.time_end}")
                            del data[c][count]
                            flag = False
                            break
                        if re.check_report_overlap2(i):
                            print("Дата выходит за пределы конференции")
                            del data[c][count]
                            flag = False
                            break
                    count += 1
                if flag:
                    print(f"Вы успешно добавили доклад:\nНазвание: {re.name}\nПродолжительность: {re.time()}")
            else:
                print("Нет такой конференции")
        elif "время самого продолжительного перерыва между докладами" in answer.lower():
            name = input("Введите название конференции: ")
            for i in data:
                if name == i.name:
                    print(i.max_break())
                    break
        elif "выйти" in answer.lower():
            break


if __name__ == "__main__":
    main()
