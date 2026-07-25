#=========================================
#دانشجو : مبین شاطری
# شماره دانشجویی : 404130803
# عنوان پروژه : شبیه سازی جام جهانی
# تاریخ تحویل : 1405/05/03
#=========================================

from Match_class import Match
import random


class Group:
    """
    کلاسی برای مدیریت مراحل گروهی با ویژگی های نام گروه و لیستی از تیم ها
    """
    def __init__(self, name, teams):
        """
        مقدار دهی اولیه ویژگی ها
        """
        self._name = name
        self._teams = teams


    @property
    def name(self):
        return self._name

    @property
    def teams(self):
        return self._teams


    def play_all_matches(self):
        """
        انجام تمام مسابقات گروه تبدیل دو تیم به یک مچ و انجام بازی بروزرسانی امار
        """
        n = len(self._teams)
        for i in range(n):
            for j in range(i + 1, n):
                match = Match(self._teams[i], self._teams[j])
                match.play()


    def get_ranking(self):
        """
        رنک بندی تیم ها بر اساس امتیاز و تفاضل گل و گل های زده در غیر این صورت شانسی
        returns: برگرداندن رنکیمگ گروه به صورت لیست
        """
        ranked = list(self._teams)
        random.shuffle(ranked)
        ranked.sort(
            key=lambda x: (x.points, x.goal_difference(), x.goals_for),
            reverse=True
        )
        return ranked


    def advance_teams(self):
        """
        برگرداندن دو تیم اول گروه بر اساس ارایه های لیست
        :return:
        """
        r = self.get_ranking()
        return r[0], r[1]
