#=========================================
#دانشجو : مبین شاطری
# شماره دانشجویی : 404130803
# عنوان پروژه : شبیه سازی جام جهانی
# تاریخ تحویل : 1405/05/03
#=========================================

from Team_class import Team


class Match:
    """
    برگزاری مسابقه بین تو تیم و بروز رسانی امار تیم ها با ویژگی های تیم اول  و دوم و
    حذفی بودن یا نبودن و برنده و گل های تیم اول و دوم و پنالتی های تیم اول و دوم
    """
    def __init__(self, team1, team2, is_knockout=False):
        """مقدار دهی اولیه ویژگی ها"""
        self._team1 = team1
        self._team2 = team2
        self._is_knockout = is_knockout
        self._winner = None
        self._goals1 = 0
        self._goals2 = 0
        self._penalty1 = None
        self._penalty2 = None


    @property
    def team1(self):
        return self._team1

    @property
    def team2(self):
        return self._team2

    @property
    def is_knockout(self):
        return self._is_knockout

    @property
    def winner(self):
        return self._winner

    @property
    def goals1(self):
        return self._goals1

    @property
    def goals2(self):
        return self._goals2

    @property
    def penalty1(self):
        return self._penalty1

    @property
    def penalty2(self):
        return self._penalty2


    def play(self):
        """
        انجام مسابقه بین دو تیم بروز رسانی امار تیم ها در مرحله گروهی
        returns: برگرداندن متغییر از کلاس تیم به عنوان برنده و در مراحل گروه در صورت تساوی None
        """
        result = self._team1.simulate_match(self._team2, self._is_knockout)

        if len(result) == 3:
            win_name, g2, g1 = result
            p1 = p2 = None
        else:
            win_name, g2, g1, p1, p2 = result

        self._goals1 = g1
        self._goals2 = g2
        self._penalty1 = p1
        self._penalty2 = p2

        if win_name == self._team1.name:
            self._winner = self._team1
        elif win_name == self._team2.name:
            self._winner = self._team2
        else:
            self._winner = None

        self._team1._goals_for += self._goals1
        self._team1._goals_against += self._goals2
        self._team2._goals_for += self._goals2
        self._team2._goals_against += self._goals1

        if not self._is_knockout:
            if self._winner == self._team1:
                self._team1._points += 3
            elif self._winner == self._team2:
                self._team2._points += 3
            else:
                self._team1._points += 1
                self._team2._points += 1

        return self._winner
