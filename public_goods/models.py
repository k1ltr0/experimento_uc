from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)
import random


class Constants(BaseConstants):
    name_in_url = "public_goods"
    players_per_group = 4
    num_rounds = 1
    endowment = c(100)
    multiplier = 2
    AdminReport_template = "public_goods/AdminReport.html"
    instructions_template = "public_goods/instructions.html"
    gamescripts = "public_goods/gamescripts.html"
    answerinput = "public_goods/answerinput.html"


class Subsession(BaseSubsession):
    def vars_for_admin_report(self):
        # contributions = [
        #     p.contribution for p in self.get_players()
        #     if p.contribution is not None
        # ]
        # if contributions:
        #     return {
        #         "avg_contribution": sum(contributions) / len(contributions),
        #         "min_contribution": min(contributions),
        #         "max_contribution": max(contributions),
        #     }
        # else:
        return {
            "avg_contribution": "(no data)",
            "min_contribution": "(no data)",
            "max_contribution": "(no data)",
        }

    def get_better_or_not(self, player):
        others = []
        for p in self.get_players():
            if p.id != player.id:
                others.append(p)

        player.better_or_not = player.correct_answers_round_three > \
            random.choice(others).correct_answers_round_three
        return player.better_or_not

    def get_ranking(self, player):

        round_one_ranking = []
        round_two_ranking = []
        round_three_ranking = []

        for p in self.get_players():
            me = False
            if p.id == player.id:
                me = True

            round_one_ranking.append(
                {"player": p.id_in_group, "answers": p.correct_answers_round_one, "me": me}
            )
            round_two_ranking.append(
                {"player": p.id_in_group, "answers": p.correct_answers_round_two, "me": me}
            )
            round_three_ranking.append(
                {"player": p.id_in_group, "answers": p.correct_answers_round_three, "me": me}
            )

        round_one_ranking = sorted(round_one_ranking, key=lambda i: i["answers"])
        round_two_ranking = sorted(round_two_ranking, key=lambda i: i["answers"])
        round_three_ranking = sorted(
            round_three_ranking, key=lambda i: i["answers"]
        )

        return {
            "1": round_one_ranking,
            "2": round_two_ranking,
            "3": round_three_ranking
        }


class Group(BaseGroup):
    total_contribution = models.CurrencyField()
    individual_share = models.CurrencyField()

    def get_best_round(self, players, field):
        best = players[0]
        for p in players:
            if getattr(p, field) > getattr(best, field):
                best = p
            if getattr(p, field) == getattr(best, field):
                best = random.choice([best, p])
        return best

    def set_payoffs(self):
        # self.total_contribution = sum(
        #     [p.contribution for p in self.get_players()]
        # )
        # self.individual_share = (
        #     self.total_contribution * Constants.multiplier /
        #     Constants.players_per_group
        # )
        for p in self.get_players():

            p.rounds_earnings = 0
            # p.payoff = (
            #     Constants.endowment - p.contribution
            # ) + self.individual_share
            p.final_round_selected = random.choice(range(1, 21))
            # p.round_selected_for_payment = 4  # random.choice([1,2,3,4,5,6,7,8])

            if p.round_selected_for_payment == 1:
                best = self.get_best_round(self.get_players(), "correct_answers_round_one")
                if best == p:
                    p.rounds_earnings = 1000 * p.correct_answers_round_one
            elif p.round_selected_for_payment == 2:
                # para etapa 1
                # 250 por pago por respuesta o
                # 1000 por pregunta si resulve mas que los demas
                if p.round_two_mode == "torneo":
                    best = self.get_best_round(self.get_players(), "correct_answers_round_two")
                    if best == p:
                        p.rounds_earnings = 1000 * p.correct_answers_round_two
                else:
                    p.rounds_earnings = 250 * p.correct_answers_round_two
            elif p.round_selected_for_payment == 3:
                # 250 por respuesta
                p.rounds_earnings = 250 * p.correct_answers_round_three
            elif p.round_selected_for_payment == 4:
                # para etapa 3
                # 250 por pago por respuesta o
                # 1000 por pregunta si es el 1
                if p.round_four_mode == "torneo":
                    best = self.get_best_round(self.get_players(), "correct_answers_round_three")
                    if best == p:
                        p.rounds_earnings = 1000 * p.correct_answers_round_three
                else:
                    p.rounds_earnings = 250 * p.correct_answers_round_three
            elif p.round_selected_for_payment == 5:
                pass
                # segun formula
            elif p.round_selected_for_payment == 6:
                pass
                # segun formula
            elif p.round_selected_for_payment == 7:
                # para etapa 3
                # 250 por pago por respuesta o
                # 1000 por pregunta si es el 1
                if p.round_seven_mode == "torneo":
                    best = self.get_best_round(self.get_players(), "correct_answers_round_three")
                    if best == p:
                        p.rounds_earnings = 1000 * p.correct_answers_round_three
                else:
                    p.rounds_earnings = 250 * p.correct_answers_round_three
            elif p.round_selected_for_payment == 8:
                pass
                # segun formula

            # final round
            p.final_round_win_lotery = "no gana"
            p.final_round_total = 0
            p.final_round_type = getattr(p, "final_round_%s" % p.final_round_selected)
            if p.final_round_type == "":
                p.final_round_type = "loteria"

            if p.final_round_type != "loteria":
                p.final_round_total = int(p.final_round_type.replace("$", "").replace(".", ""))
            else:
                p.final_round_total = random.choice([0, 5000])
                if p.final_round_total == 5000:
                    p.final_round_win_lotery = "gana"

            p.payoff = p.final_round_total + p.rounds_earnings


class Player(BasePlayer):
    # contribution = models.CurrencyField(
    #     doc="The amount contributed by the player",
    #     max=Constants.endowment, min=0
    # )

    participant_code = models.StringField(initial="")
    correct_answers_practice = models.IntegerField(initial=0)
    correct_answers_round_one = models.IntegerField(initial=0)
    correct_answers_round_two = models.IntegerField(initial=0)
    correct_answers_round_three = models.IntegerField(initial=0)

    probabilities_round_five_0 = models.IntegerField(initial=25)
    probabilities_round_five_1 = models.IntegerField(initial=25)
    probabilities_round_five_2 = models.IntegerField(initial=25)
    probabilities_round_five_3 = models.IntegerField(initial=25)

    better_or_not = models.BooleanField(initial=False)
    probabilities_round_six_0 = models.IntegerField(initial=25)
    probabilities_round_six_1 = models.IntegerField(initial=25)
    probabilities_round_six_2 = models.IntegerField(initial=25)
    probabilities_round_six_3 = models.IntegerField(initial=25)

    probabilities_round_eight_0 = models.IntegerField(initial=25)
    probabilities_round_eight_1 = models.IntegerField(initial=25)
    probabilities_round_eight_2 = models.IntegerField(initial=25)
    probabilities_round_eight_3 = models.IntegerField(initial=25)

    round_selected_for_payment = models.IntegerField(initial=0)
    final_round_selected = models.IntegerField(initial=0)
    final_round_type = models.StringField(initial="loteria")
    final_round_win_lotery = models.StringField(initial="no gana")
    final_round_total = models.IntegerField(initial=0)

    final_round_1 = models.StringField(choices=["$200", "loteria"], widget=widgets.RadioSelect, initial="loteria")
    final_round_2 = models.StringField(choices=["$400", "loteria"], widget=widgets.RadioSelect, initial="loteria")
    final_round_3 = models.StringField(choices=["$600", "loteria"], widget=widgets.RadioSelect, initial="loteria")
    final_round_4 = models.StringField(choices=["$800", "loteria"], widget=widgets.RadioSelect, initial="loteria")
    final_round_5 = models.StringField(choices=["$1.000", "loteria"], widget=widgets.RadioSelect, initial="loteria")
    final_round_6 = models.StringField(choices=["$1.200", "loteria"], widget=widgets.RadioSelect, initial="loteria")
    final_round_7 = models.StringField(choices=["$1.400", "loteria"], widget=widgets.RadioSelect, initial="loteria")
    final_round_8 = models.StringField(choices=["$1.600", "loteria"], widget=widgets.RadioSelect, initial="loteria")
    final_round_9 = models.StringField(choices=["$1.800", "loteria"], widget=widgets.RadioSelect, initial="loteria")
    final_round_10 = models.StringField(choices=["$2.000", "loteria"], widget=widgets.RadioSelect, initial="loteria")
    final_round_11 = models.StringField(choices=["$2.200", "loteria"], widget=widgets.RadioSelect, initial="loteria")
    final_round_12 = models.StringField(choices=["$2.400", "loteria"], widget=widgets.RadioSelect, initial="loteria")
    final_round_13 = models.StringField(choices=["$2.600", "loteria"], widget=widgets.RadioSelect, initial="loteria")
    final_round_14 = models.StringField(choices=["$2.800", "loteria"], widget=widgets.RadioSelect, initial="loteria")
    final_round_15 = models.StringField(choices=["$3.000", "loteria"], widget=widgets.RadioSelect, initial="loteria")
    final_round_16 = models.StringField(choices=["$3.200", "loteria"], widget=widgets.RadioSelect, initial="loteria")
    final_round_17 = models.StringField(choices=["$3.400", "loteria"], widget=widgets.RadioSelect, initial="loteria")
    final_round_18 = models.StringField(choices=["$3.600", "loteria"], widget=widgets.RadioSelect, initial="loteria")
    final_round_19 = models.StringField(choices=["$3.800", "loteria"], widget=widgets.RadioSelect, initial="loteria")
    final_round_20 = models.StringField(choices=["$4.000", "loteria"], widget=widgets.RadioSelect, initial="loteria")

    rounds_earnings = models.IntegerField(initial=0)

    round_two_mode = models.StringField(
        choices=[
            ["por respuesta", "Pago por respuesta ($250 por cada suma correcta)"],
            ["torneo", "Torneo ($1000 por cada suma correcta si resuelves más sumas correctas que los otros miembros en la Tarea 1, en caso contrario recibes $0)."]
        ],
        widget=widgets.RadioSelect,
        initial="por respuesta"
    )

    round_four_mode = models.StringField(
        choices=[
            ["por respuesta", (
                "1. Pago por Pregunta ($250 por cada suma correcta en Etapa 3)"
            )],
            ["torneo", (
                "2. Torneo ($1000 por cada suma correcta si resolviste más "
                "sumas correctas que el resto de los participantes en la "
                "Etapa 3. En caso contrario, recibirás $0)"
            )]
        ],
        widget=widgets.RadioSelect,
        initial="por respuesta"
    )

    round_seven_mode = models.StringField(
        choices=[
            ["por respuesta", (
                "1. Tarifa por Pregunta ($250 por cada suma correcta en la "
                "Etapa 3)."
            )],
            ["torneo", (
                "2. Torneo pagado ($1.000 por cada suma correcta SI resolviste"
                " más sumas que los otros miembros del grupo en la Tarea 3, y "
                "$ 0 de lo contrario)."
            )],
        ],
        widget=widgets.RadioSelect,
        initial="por respuesta"
    )
