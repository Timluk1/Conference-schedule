import datetime as dt

data = {}
ends = {}


class Report:
    def __init__(self, name, conference, start, end):
        self.conference = conference
        self.time_start = dt.datetime.strptime(start, "%Y:%m:%d,%H:%M")
        self.time_end = dt.datetime.strptime(end, "%Y:%m:%d,%H:%M")
        self.name = name
        data[conference].append(self)

    def check_report_overlap(self, new_report):
        return (self.time_start <= new_report.time_start <= self.time_end) and \
               (self.time_start <= new_report.time_end <= self.time_end)

    def check_report_overlap2(self, conference):
        return (conference.start <= self.time_start <= conference.end) and \
               (conference.start <= self.time_end <= conference.end)

    def time(self):
        return self.time_end - self.time_start


class Conference:
    def __init__(self, name, start, end, topic):
        global data
        self.name = name
        self.start = dt.datetime.strptime(start, "%Y:%m:%d,%H:%M")
        self.end = dt.datetime.strptime(end, "%Y:%m:%d,%H:%M")
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
        max_break_duration = max([data2[i + 1].time_start - data2[i].time_end for i in range(len(data2) - 1)])
        max_break_duration_str = str(max_break_duration.days) + " days, " + str(
            max_break_duration.seconds // 3600) + " hours, " + str((max_break_duration.seconds // 60) % 60) + " minutes"
        return max_break_duration_str

    def reports(self):
        return data[self]


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
    while True:
        print("Здравствуйте, вы можете создать конференцию и загрузить доклады по конференции.")
        print(
            "Команды:\nВывезти прошедшие конференции\nВывезти идущие конференции\nДобавить конференцию\nДобавить доклад"
            " в конференцию\nВремя самого продолжительного перерыва между докладами\nВывезти доклады конференции\nВыйти"
        )
        answer = input("Введите команду: ")
        if "добавить конференцию" in answer.lower():
            name_conference = input("Введите название конференции: ")
            topic_conference = input("Введите тему конференции: ")
            start = input(
                "Введите дату начала конференции, пример: 2024:12:02,10:0, формат (год, месяц, день, часы, минуты): ")
            end = input(
                "Введите дату окончания конференции, пример: 2024:12:02,10:0, формат (год, месяц, день, часы, минуты): "
            )
            Conference(name_conference, start, end, topic_conference)
            print("Конференция добавлена!")
        elif "вывезти идущие конференции" in answer.lower():
            delete_end_conferences()
            if data == {}:
                print()
                print("Нет идущих конференций")
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
                    "Введите дату начала доклада, пример: 2024:12:02,10:0, формат (год, месяц, день, часы, минуты): ")
                end = input(
                    "Введите дату окончания доклада, пример: 2024:12:02,10:0, формат (год, месяц, день, часы, минуты): ")
                name = input("Введите название доклада: ")
                re = Report(name, c, start, end)
                flag = True
                if not re.check_report_overlap2(c):
                    print("Дата выходит за пределы конференции")
                    del data[c][data[c].index(re)]
                    flag = False
                if len(data[c]) != 1:
                    for i in data[c]:
                        if i != re:
                            if i.check_report_overlap(re):
                                print(
                                    f"Дата перекрывает уже существующую дату: "
                                    f"{i.time_start.strftime('%B %d, %Y')}, {i.time_start.strftime('%H:%M')}"
                                    f"- {i.time_end.strftime('%B %d, %Y')}, {i.time_end.strftime('%H:%M')}")
                                del data[c][data[c].index(re)]
                                flag = False
                                break
                if flag:
                    print(f"Вы успешно добавили доклад:\nНазвание: {re.name}\nПродолжительность: {re.time()}")
            else:
                print("Нет такой конференции")
        elif "время самого продолжительного перерыва между докладами" in answer.lower():
            name = input("Введите название конференции: ")
            flag = True
            for i in data:
                if name == i.name:
                    print(i.max_break())
                    flag = False
                    break
            if flag:
                print()
                print("К сожалени нет такой конференции")
        elif "Вывезти доклады конференции":
            name_conference = input("Введите название конференции: ")
            print("Доступные конференции: ")
            for i in data:
                print()
                i.active_confernces()
            print()
            conf = [i for i in data if i.name == name_conference]
            if len(conf) != 0:
                r = conf[0].reports()[0]
                duration = r.time()
                print(
                    f"Название: {name}"
                    f"Начало: {r.time_start.strftime('%B %d, %Y')}, {r.time_start.strftime('%H:%M')}\n"
                    f"Конец: {r.time_end.strftime('%B %d, %Y')}, {r.time_end.strftime('%H:%M')}\n"
                    f"Продолжительность: {str(duration.days)} days, {str(duration.seconds // 3600)} hours,"
                    f"{str((duration.seconds // 60) % 60)} minutes"
                )
        elif "выйти" in answer.lower():
            break


if __name__ == "__main__":
    main()
