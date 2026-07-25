#=========================================
#دانشجو : مبین شاطری
# شماره دانشجویی : 404130803
# عنوان پروژه : شبیه سازی جام جهانی
# تاریخ تحویل : 1405/05/03
#=========================================

import random
import numpy as np


class Team:
    """
    کلاس تیم فوتبال با ویژگی های اسم و قدرت حمله و قدرت دفاع و رتبه و گل زده و گل خورده و امتیاز و گروه
    ومتود های صفر کردن امار تیم و تفاضل گل و شبیه سازی مسابقه
    """
    def __init__(self, name, attack, defense, rank,goals_for=0, goals_against=0,points=0, group=None):
        """
        مقدار دهی اولیه ویژگی ها
        """
        self._name = name
        self._attack = attack
        self._defense = defense
        self._rank = rank

        self._goals_for = goals_for
        self._goals_against = goals_against
        self._points = points
        self._group = group


    @property
    def name(self):
        return self._name

    @property
    def attack(self):
        return self._attack

    @property
    def defense(self):
        return self._defense

    @property
    def rank(self):
        return self._rank

    @property
    def goals_for(self):
        return self._goals_for

    @property
    def goals_against(self):
        return self._goals_against

    @property
    def points(self):
        return self._points

    @property
    def group(self):
        return self._group

    @group.setter
    def group(self, value):
        self._group = value


    def goal_difference(self):
        """
        محاسبه تفاضل گل با منها کردن گل زده و خورده
        :return: برگرداندن تفاضل
        """
        return self._goals_for - self._goals_against


    def reset_stats(self):
        """
        صفر کردن امار تیم ها
        """
        self._goals_for = 0
        self._goals_against = 0
        self._points = 0


    def shoot_penalty(self, opponent):
        """
        تابعی برای انجام پنالتی
        پارامتر: opponent(تیم حریف)
        returns:مقدار ترو در صورت گل شدن و مقدار فالس در صورت گل نشدن
        """
        p = 0.75 + (self._attack - opponent.defense) / 250
        p = max(0.6, min(0.9, p))
        return random.random() < p


    def simulate_match(self, opponent, is_knockout=False):
        """
        شبیه سازی مسابقه فوتبال چه در مراحل گروهی چه در مراحل حذفی
        پارامتر:opponent(تیم حریف) و is_knockout(ایا حذفی است یا خیر)
        returns:برگرداندن تاپل سه تایی شکال تیم برنده و گل ها در مراحل گروهی و برگرداندن تاپل پنج تایی در صورت داشتن پنالتی در مراحل حذفی
        """
        lambda_self = (self._attack / 100) * 1.5 + (1 - opponent.defense / 100) * 0.8
        lambda_opponent = (opponent.attack / 100) * 1.5 + (1 - self._defense / 100) * 0.8

        self_goals = np.random.poisson(lambda_self)
        opponent_goals = np.random.poisson(lambda_opponent)

        if not is_knockout:
            if self_goals > opponent_goals:
                winner = self._name
            elif opponent_goals > self_goals:
                winner = opponent.name
            else:
                winner = "draw"
            return (winner, opponent_goals, self_goals, None, None)

        if self_goals > opponent_goals:
            return (self._name, opponent_goals, self_goals, None, None)

        if opponent_goals > self_goals:
            return (opponent.name, opponent_goals, self_goals, None, None)

        extra_self = np.random.poisson(lambda_self * 0.33)
        extra_opp = np.random.poisson(lambda_opponent * 0.33)
        self_goals += extra_self
        opponent_goals += extra_opp

        if self_goals > opponent_goals:
            return (self._name, opponent_goals, self_goals, None, None)

        if opponent_goals > self_goals:
            return (opponent.name, opponent_goals, self_goals, None, None)

        s_self, s_opp = 0, 0
        left_self, left_opp = 5, 5

        for _ in range(5):
            left_self -= 1
            if self.shoot_penalty(opponent):
                s_self += 1
            if s_self > s_opp + left_opp:
                return (self._name, opponent_goals, self_goals, s_self, s_opp)

            left_opp -= 1
            if opponent.shoot_penalty(self):
                s_opp += 1
            if s_opp > s_self + left_self:
                return (opponent.name, opponent_goals, self_goals, s_self, s_opp)
            if s_self > s_opp + left_self:
                return (self._name, opponent_goals, self_goals, s_self, s_opp)

        while True:
            a = self.shoot_penalty(opponent)
            b = opponent.shoot_penalty(self)
            if a and not b:
                s_self += 1
                return (self._name, opponent_goals, self_goals, s_self, s_opp)
            if b and not a:
                s_opp += 1
                return (opponent.name, opponent_goals, self_goals, s_self, s_opp)
