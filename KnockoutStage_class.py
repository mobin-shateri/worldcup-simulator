#=========================================
#دانشجو : مبین شاطری
# شماره دانشجویی : 404130803
# عنوان پروژه : شبیه سازی جام جهانی
# تاریخ تحویل : 1405/05/03
#=========================================

from Match_class import Match


class KnockoutStage:
    """
    کلاسی برای مدیریت مسابقات مراحل حذفی با ویژگی های نام مرحله گروهی و لیستی از مسابقات اان مرحله
    """
    def __init__(self, round_name, matches):
        """
        مقدار دهی اولیه ویژگی ها
        """
        self._round_name = round_name
        self._matches = matches


    @property
    def round_name(self):
        return self._round_name
    @property
    def matches(self):
        return self._matches


    def play_round(self):
        """
        انجام تمام مسابقات با استفاده از حلقه فور روی لیست مچ ها
        """
        for match in self._matches:
            match.play()


    def get_winners(self):
        """
        پیدا کردن برمده های مرحله حذفی با در لیست
        returns: برگرداندن لیستی از برنده ها
        """
        return  [match.winner for match in self._matches]


    def display_results(self):
        """
        نشان دادن نتیجه با نمایش پنالتی ها و هم چنین برند ها با حلقه فور با اف استرینگ
        returns: چاپ نتایج مراحل حذفی
        """
        print(f"====={self._round_name}=====")
        for match in self._matches:
            team1_name = match.team1.name
            team2_name = match.team2.name
            score_text = f"{team1_name} {match.goals1} - {match.goals2} {team2_name}"

            if match.penalty1 is not None and match.penalty2 is not None:
                score_text += f" (pens {match.penalty1}-{match.penalty2})"

            winner_name = match.winner.name if match.winner else "None"
            print(f"{score_text} => {winner_name}")

