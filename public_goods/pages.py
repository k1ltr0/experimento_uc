from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import random


class Welcome(Page):
    pass


class PracticeIntro(Page):
    pass


class Introduction(Page):
    pass


class PracticeGame(Page):
    form_model = "player"
    form_fields = ["correct_answers_practice"]
    timeout_seconds = 120
    timer_text = "Tiempo restante"
    timeout_submission = {'accept': True}


class RoundOneIntro(Page):
    pass


class RoundOneGame(Page):
    form_model = "player"
    form_fields = ["correct_answers_round_one"]
    timeout_seconds = 240
    timer_text = "Tiempo restante"
    timeout_submission = {'accept': True}


class RoundTwoIntro(Page):
    form_model = "player"
    form_fields = ["round_two_mode"]


class RoundTwoGame(Page):
    form_model = "player"
    form_fields = ["correct_answers_round_two"]
    timeout_seconds = 240
    timer_text = "Tiempo restante"
    timeout_submission = {'accept': True}


class RoundThreeIntro(Page):
    pass


class RoundThreeGame(Page):
    form_model = "player"
    form_fields = ["correct_answers_round_three"]
    timeout_seconds = 240
    timer_text = "Tiempo restante"
    timeout_submission = {'accept': True}


class RoundFourIntro(Page):
    pass


class RoundFourGame(Page):
    form_model = "player"
    form_fields = ["round_four_mode"]


class RoundFiveGame(Page):
    form_model = "player"
    form_fields = [
        "probabilities_round_five_0",
        "probabilities_round_five_1",
        "probabilities_round_five_2",
        "probabilities_round_five_3"
    ]


class RoundSixIntro(Page):
    form_model = "player"
    form_fields = [
        "probabilities_round_six_0",
        "probabilities_round_six_1",
        "probabilities_round_six_2",
        "probabilities_round_six_3"
    ]

    def vars_for_template(self):
        return {"isbetter": self.subsession.get_better_or_not(self.player)}


class RoundSevenIntro(Page):
    pass


class RoundEightIntro(Page):
    pass


class RoundNineIntro(Page):
    pass


# undefined
class Contribute(Page):
    form_model = "player"
    form_fields = ["contribution"]


class WaitForGame(WaitPage):
    body_text = "Esperando a los otros jugadores."


class ResultsWaitPage(WaitPage):
    body_text = "Esperando a los otros jugadores."

    def after_all_players_arrive(self):
        self.group.set_payoffs()


class Results(Page):
    def vars_for_template(self):
        # return {"total_earnings":
        # self.group.total_contribution * Constants.multiplier}
        return {"total_earnings": 1}


page_sequence = [
    Welcome,
    PracticeIntro,
    WaitForGame,
    PracticeGame,

    RoundOneIntro,
    WaitForGame,
    RoundOneGame,
    WaitForGame,

    RoundTwoIntro,
    WaitForGame,
    RoundTwoGame,
    WaitForGame,

    RoundThreeIntro,
    WaitForGame,
    RoundThreeGame,
    WaitForGame,

    RoundFourIntro,
    RoundFourGame,
    WaitForGame,

    RoundFiveGame,
    WaitForGame,

    RoundSixIntro,
    WaitForGame,

    RoundSevenIntro,
    WaitForGame,

    RoundEightIntro,
    WaitForGame,

    RoundNineIntro,
    WaitForGame,

    ResultsWaitPage,
    Results
]
