#=========================================
#دانشجو : مبین شاطری
# شماره دانشجویی : 404130803
# عنوان پروژه : شبیه سازی جام جهانی
# تاریخ تحویل : 1405/05/03
#=========================================

import csv
import os
import random
from Team_class import Team
from Match_class import Match
from Group_class import Group
from KnockoutStage_class import KnockoutStage


class WorldCupSimulator:
    """
    کلاس اصلی شامل خواندن از فایل و انجام تمام مراحل جام و شبیه سازی چندین باره با ویژگی های لیست تیم ها  و لیست گروه ها
    مرحله یک شانزدهم و مرحله یک چهارم و نیمه نهایی و فینال و قهرمان
    """
    def __init__(self):
        """
        مقدار دهی اولیه ویژگی ها
        """
        self._teams = []
        self._groups = []
        self._round_of_16 = None
        self._quarterfinals = None
        self._semifinals = None
        self._final = None
        self._champion = None


    @property
    def teams(self):
        return self._teams

    @property
    def groups(self):
        return self._groups

    @property
    def round_of_16(self):
        return self._round_of_16

    @property
    def quarterfinals(self):
        return self._quarterfinals

    @property
    def semifinals(self):
        return self._semifinals

    @property
    def final(self):
        return self._final

    @property
    def champion(self):
        return self._champion


    def load_teams_from_csv(self, filename):
        """
        خواندن فایل با بررسی وجود فایل و مدیریت خطا با ترای و اکسپت و بررسی خالی نبودن فایل و ساخت کلاس تیم
        returns: برگرداندن مقدار فالس در صورت نبود فایل و خالی بودن فایل و ارور های رایج و مقدار ترو در صورت اد شدن تیم ها
        """

        if not os.path.exists(filename):
            print(f"{filename} does not exist")
            return False

        try:
            loaded_team = []
            with open(filename, mode='r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    team = Team(row["name"].strip(), int(row["attack"]), int(row["defense"]), int(row["rank"]))
                    loaded_team.append(team)

            if len(loaded_team) == 0:
                print("the csv file is empty or has an invalid structure")
                return False
            self._teams = loaded_team
            print(f"loaded {len(loaded_team)} teams successfully")
            return True
        except(csv.Error, KeyError, ValueError) as error:
            print(f"error while loading csv file:{error}")
            return False


    def seed_and_draw_groups(self):
        """
        تابعی که ابتدا سید تیم ها را بر اساس رنک انها در چهار سید قرار میدهد و با استفاده از حلقه و دیکشنری انها را
        به 8 گروه تقسیم میکند(کلاس گروه) و لیستی از گروه ها را ذخیره میکند
        returns: بر گرداندن مقادیر فالس در صورتی که تیم ها اضافه نشده باشند و مقدار انها 32 تا نباشد و برگرداندن ترو در صورتی
        که گروه بندی انجام شده باشد
        """
        if not self._teams:
            print("please load the teams first")
            return False

        if len(self._teams) != 32:
            print("Exactly 32 teams are required.")
            return False

        sorted_teams = sorted(self._teams, key=lambda x: x.rank)
        seed_1 = sorted_teams[0:8]
        seed_2 = sorted_teams[8:16]
        seed_3 = sorted_teams[16:24]
        seed_4 = sorted_teams[24:32]

        group_names = ["A", "B", "C", "D", "E", "F", "G", "H"]
        group_teams_map = {name: [] for name in group_names}

        for seed in (seed_1, seed_2, seed_3, seed_4):
            shuffled_seed = random.sample(seed, len(seed))

            for group_name, team in zip(group_names, shuffled_seed):
                team.group = group_name
                group_teams_map[group_name].append(team)

        self._groups = [Group(name, group_teams_map[name]) for name in group_names]

        return True


    def run_group_stage(self):
        """
        انجام تمام مسابقات هر گروه و چاپ جدول ان بصورت مرتب با اف استرینگ
        :return: مقدار فالس در صورت انجام نشدن قرعه کشی و مقدار ترو در صورت انجام تمام مراحل
        """
        if not self._groups:
            print("please draw the groups first")
            return False

        for group in self._groups:
            group.play_all_matches()
            ranking = group.get_ranking()

            print(f"\nGroup {group.name}")
            print("-" * 50)
            # Creating a fixed-width header
            print(f"{'Pos':<5}{'Team':<20}{'Pts':>6}{'GD':>8}{'GF':>8}")
            print("-" * 50)

            for rank, team in enumerate(ranking, start=1):
                gd = team.goal_difference()
                gd_text = f"+{gd}" if gd > 0 else str(gd)

                print(f"{rank:<5}{team.name:<20}{team.points:>6}{gd_text:>8}{team.goals_for:>8}")

        return True



    def setup_knockout_bracket(self):
        """
        مشخص کردن براکت حدفی و مشخص کردن بازی ها براساس قانون فیفا بصورت لیستی از تاپل ها تبدیل انها به کلاس مچ
        returns: مقدار فالس در صورت اجرا نکردن مرحله گروهی و مقدار ترو در صورت تعیین براکت حذفی
        """
        if not self._groups:
            print("please run the group stage first")
            return False

        group_map = {group.name: group for group in self._groups}
        firsts = {}
        seconds = {}
        for name, group in group_map.items():
            first_team, second_team = group.advance_teams()
            firsts[name] = first_team
            seconds[name] = second_team

        pairings = [(firsts["A"], seconds["B"]), (firsts["C"], seconds["D"]), (firsts["E"], seconds["F"]),
                    (firsts["G"], seconds["H"]), (firsts["B"], seconds["A"]), (firsts["D"], seconds["C"]),
                    (firsts["F"], seconds["E"]), (firsts["H"], seconds["G"])]

        matches = [Match(team1, team2, is_knockout=True) for team1, team2 in pairings]
        self._round_of_16 = KnockoutStage("Round of 16", matches)
        return True


    def run_knockout_stage(self):
        """
        اجرای تمامی بازی های حذفی تا رسیدن به فینال با ویژگی های کلاس های مپ و ناک اوت استیج
         returns: مقدار None در صورت انجام ندادن براکت حذفی
         و برگرداندن قهرمان در صورت انجام تمام مراحل
        """
        if self._round_of_16 is None:
            print("Please set up the knockout bracket first.")
            return None

        self._round_of_16.play_round()
        r16_winners = self._round_of_16.get_winners()

        quarter_matches = [Match(r16_winners[i], r16_winners[i + 1], is_knockout=True) for i in
                           range(0, len(r16_winners), 2)]
        self._quarterfinals = KnockoutStage("Quarterfinals", quarter_matches)
        self._quarterfinals.play_round()
        qf_winners = self._quarterfinals.get_winners()

        semi_matches = [Match(qf_winners[i], qf_winners[i + 1], is_knockout=True) for i in range(0, len(qf_winners), 2)]
        self._semifinals = KnockoutStage("Semifinals", semi_matches)
        self._semifinals.play_round()
        sf_winners = self._semifinals.get_winners()

        final_matches = [Match(sf_winners[i], sf_winners[i + 1], is_knockout=True) for i in
                         range(0, len(sf_winners), 2)]
        self._final = KnockoutStage("Final", final_matches)
        self._final.play_round()
        final_winners = self._final.get_winners()

        self._champion = final_winners[0]
        return self._champion


    def run_full_simulation(self):
        """
        ابتدا اممار را صفر میکند تمامی مراحل را انجام میدهد و در نهایت قهرمان را بر میگرداند
        return: برگرداندن مقدار None در صورتی که تیم ها اد نشده باشند و و همچنین هر کدام از مراحل قرعه کشی و
        انجام مرحله گروهی و براکت انجام نوشود و برگرداندن قهرمان در صورت انجام تمام مراحل
        """
        if not self._teams:
            print("Please load the teams first.")
            return None

        for team in self._teams:
            team.reset_stats()

        if not self.seed_and_draw_groups():
            return None
        if not self.run_group_stage():
            return None
        if not self.setup_knockout_bracket():
            return None

        champion = self.run_knockout_stage()
        if champion:
            print(f"\nWorld Cup champion: {champion.name}")
        return champion


    def run_full_simulation2(self):
        """
        متدی شبیه متد run_full_simulation
        بدون پرینت کردن چیزی برای استفاده در شبیه سازی هزار باره
        """
        for team in self._teams:
            team.reset_stats()

        if not self.seed_and_draw_groups():
            return None

        for group in self._groups:
            group.play_all_matches()

        if not self.setup_knockout_bracket():
            return None

        return self.run_knockout_stage()


    def most_likely_champion(self , num_simulations=1000):
        """
        شبیه سازی هزار باره و محاسبه تعداد قهرمانی های هر تیم و محاسبه درصد و مرتب کردن ان
        پارامتر:num_simulation (تعداد شبیه ساز)
        returns: مقدار None در صورت نبودن تیم ها و صفر یا منفی بودن تعداد شبیه سازی
        وبرگرداندن درصد ها
        """
        if not self._teams:
            print("please load the teams first")
            return None

        if num_simulations <= 0:
            print("Error: the number of simulation must be a positive number")
            return None

        champion_counts = {team.name : 0 for team in self._teams}

        for i in range(num_simulations):
            champion = self.run_full_simulation2()
            if champion:
                champion_counts[champion.name] += 1

        percentages = {name : (count / num_simulations) * 100 for name, count in champion_counts.items()}

        sorted_percentages = dict(sorted(percentages.items(), key=lambda x: x[1], reverse=True))

        print(f"\n{num_simulations} simulations completed")
        print("champion percentage per team:")
        for name , pct in sorted_percentages.items():
            if pct > 0:
                print(f"{name}: {pct:.1f}%")

        return sorted_percentages


    def display_bracket(self):
        """
        متدی برای نماش تمام مراحل حذفی و چاپ نتایج هر مرحله
        return: مقدار فالس در صورت None بودن هر کدام از مراحل
        ومقدار ترو در صورت چاپ براکت
        """
        stages = [self._round_of_16 , self._quarterfinals , self._semifinals , self._final]
        for stage in stages:
            if stage is None:
                print("please run a full simulation first")
                return False

        print("===== Knockout Bracket =====")
        for stage in stages:
            stage.display_results()

        if self._champion:
            print(f"\nchampion: {self._champion.name}")
        return True