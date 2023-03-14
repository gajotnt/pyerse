""""Helper com ciclos"""

from datetime import date, time, datetime, timedelta

from pyerse.periodos_horarios import Periodos_Horarios as ph


class Ciclo:
    """Estão previstos dois ciclos: ciclo diário (os períodos horários são iguais em todos os dias do ano) e ciclo semanal (os períodos horários diferem entre dias úteis e fim de semana)."""

    @classmethod
    def in_time_range(cls, hour_start, minute_start, t, hour_stop, minute_stop):
        if hour_stop < hour_start:
            return not (
                time(hour_stop, minute_stop)
                <= t.time()
                < time(hour_start, minute_start)
            )
        return time(hour_start, minute_start) <= t.time() < time(hour_stop, minute_stop)

    @classmethod
    def is_summer(cls, time):
        # Hora legal de Verão começa no 1º Domingo de Março e acaba no ultimo de Outubro
        # https://docs.python.org/3.3/library/datetime.html
        d = datetime(time.year, 4, 1)
        i_verao = d - timedelta(days=d.weekday() + 1)
        d = datetime(time.year, 11, 1)
        f_verao = d - timedelta(days=d.weekday() + 1)
        if i_verao <= time.replace(tzinfo=None) < f_verao:
            return True
        return False

    @classmethod
    def get_periodo_horario(cls, time):
        """Retorna o Periodo Horario em que nos encontramos"""
        raise NotImplementedError


class Ciclo_Semanal_a(Ciclo):                                                                       #Adicionado um "_a" para diferenciar do continental
    """Ciclo semanal açores (os períodos horários diferem entre dias úteis e fim de semana)."""

    def __str__(self) -> str:
        return "Ciclo Semanal"

    @classmethod
    def get_periodo_horario(cls, time):
        if cls.is_summer(time):
            # Verão
            if 0 <= time.weekday() < 5:
                # Seg a Sex
                if cls.in_time_range(10, 30, time, 15, 30):
                    return ph.PONTA                                                 #Seg a Sex - PONTA das 10h30 às 15h30
                if cls.in_time_range(7, 0, time, 10, 30) or cls.in_time_range(
                    15, 30, time, 0, 0
                ):
                    return ph.CHEIAS                                                 #Seg a Sex - CHEIAS das 07h00 às 10h30 e das 15h30 às 24h00
                if cls.in_time_range(0, 0, time, 7, 0):
                    return ph.VAZIO_NORMAL                                                 #Seg a Sex - VAZIO das 07h00 às 10h30 e das 15h30 às 24h00
#NÂO EXISTE     if cls.in_time_range(2, 0, time, 6, 0):
#NÂO EXISTE        return ph.SUPER_VAZIO
            if time.weekday() == 5:
                # Sabado
                if cls.in_time_range(11, 0, time, 14, 30) or cls.in_time_range(
                    19, 30, time, 23, 0
                ):
                    return ph.CHEIAS                                                 #SABADO - CHEIAS das 11h00 às 14h30 e das 19h30 às 23h00
                if (
                    cls.in_time_range(0, 0, time, 11, 0)
                    or cls.in_time_range(14, 30, time, 19, 30)
                    or cls.in_time_range(23, 0, time, 0, 0)
#NÂO EXISTE         or cls.in_time_range(22, 0, time, 0, 0)
                ):
                    return ph.VAZIO_NORMAL                                                 #SABADO - VAZIO das 00h00 às 11h00, das 14h30 às 19h30 e das 23h00 às 24h00
#NÂO EXISTE     if cls.in_time_range(2, 0, time, 6, 0):
#NÂO EXISTE         return ph.SUPER_VAZIO
            if time.weekday() == 6:
                # Domingo
                if cls.in_time_range(0, 0, time, 0, 0) #REMOVIDO or cls.in_time_range(
#REMOVIDO           6, 0, time, 0, 0
                ):
                    return ph.VAZIO_NORMAL                                                 #DOMINGO - VAZIO das 00h00 às 24h00 (TODO O DIA)
#NÂO EXISTE if cls.in_time_range(2, 0, time, 6, 0):
#NÂO EXISTE         return ph.SUPER_VAZIO
        else:
            # Inverno
            if 0 <= time.weekday() < 5:
                # Seg a Sex
                if cls.in_time_range(18, 30, time, 21, 30) #REMOVIDO or cls.in_time_range(
#REMOVIDO           18, 30, time, 21, 0
                ):
                    return ph.PONTA                                                 #Seg a Sex - PONTA das 18h30 às 21h30
                if (
                    cls.in_time_range(7, 0, time, 18, 30)
                    or cls.in_time_range(21, 30, time, 0, 0)
#REMOVIDO           or cls.in_time_range(21, 0, time, 0, 0)
                ):
                    return ph.CHEIAS                                                 #Seg a Sex - CHEIAS das 07h00 às 18h30 e das 21h30 às 24h00
                if cls.in_time_range(0, 0, time, 7, 0) #REMOVIDO or cls.in_time_range(
#REMOVIDO           6, 0, time, 7, 0
                ):
                    return ph.VAZIO_NORMAL                                                 #Seg a Sex - VAZIO das 00h00 às 07h00
#NÃO EXISTE     if cls.in_time_range(2, 0, time, 6, 0):
#NÃO EXISTE         return ph.SUPER_VAZIO
            if time.weekday() == 5:
                # Sabado
                if cls.in_time_range(11, 30, time, 13, 30) or cls.in_time_range(
                    18, 0, time, 23, 0
                ):
                    return ph.CHEIAS                                                 #SABADO - CHEIAS das 11h30 às 13h30 e das 18h00 às 23h00
                if (
                    cls.in_time_range(0, 0, time, 11, 30)
                    or cls.in_time_range(13, 30, time, 18, 0)
                    or cls.in_time_range(23, 0, time, 0, 0)
#REMOVIDO           or cls.in_time_range(22, 0, time, 0, 0)
                ):
                    return ph.VAZIO_NORMAL                                                 #SABADO - VAZIO das 00h00 às 11h30, das 13h30 às 18h00 e das 23h00 às 24h00
#REMOVIDO        if cls.in_time_range(2, 0, time, 6, 0):
#REMOVIDO           return ph.SUPER_VAZIO
            if time.weekday() == 6:
                # Domingo
                if cls.in_time_range(0, 0, time, 0, 0) #REMOVIDO or cls.in_time_range(
#REMOVIDO           6, 0, time, 0, 0
                ):
                    return ph.VAZIO_NORMAL                                                 #DOMINGO - VAZIO das 00h00 às 24h00 (TODO O DIA)
#REMOVIDO       if cls.in_time_range(2, 0, time, 6, 0):
#REMOVIDO           return ph.SUPER_VAZIO


class Ciclo_Diario_a(Ciclo):                                                                       #Adicionado um "_a" para diferenciar do continental
    """Ciclo diário açores (os períodos horários são iguais em todos os dias do ano) """

    def __str__(self) -> str:
        return "Ciclo Diário"

    @classmethod
    def get_periodo_horario(cls, time):
        if cls.is_summer(time):
            # Verão
            if cls.in_time_range(9, 0, time, 11, 30) or cls.in_time_range(
                19, 30, time, 21, 0
            ):
                return ph.PONTA                                              #PONTA das 9h00 às 11h30 e das 19h30 às 21h00
            if (
                cls.in_time_range(8, 0, time, 9, 0)
                or cls.in_time_range(11, 30, time, 19, 30)
                or cls.in_time_range(21, 0, time, 22, 0)
            ):
                return ph.CHEIAS                                              #CHEIAS das 8h00 às 09h00, das 11h30 às 19h30 e das 21h00 às 22h00
            if (
                cls.in_time_range(22, 0, time, 8, 0)
#REMOVIDO       or cls.in_time_range(22, 0, time, 0, 0)
#REMOVIDO       or cls.in_time_range(0, 0, time, 2, 0)
            ):
                return ph.VAZIO_NORMAL                                              #VAZIO das 22h00 às 08h00
#NÃO EXISTE if cls.in_time_range(2, 0, time, 6, 0):
#NÃO EXISTE     return ph.SUPER_VAZIO
        else:
            # Inverno
            if cls.in_time_range(9, 30, time, 11, 0) or cls.in_time_range(
                17, 30, time, 20, 0
            ):
                return ph.PONTA                                              #PONTA das 9h30 às 11h00 e das 17h30 às 20h00
            if (
                cls.in_time_range(8, 0, time, 9, 30)
                or cls.in_time_range(11, 0, time, 17, 30)
                or cls.in_time_range(20, 0, time, 22, 0)
            ):
                return ph.CHEIAS                                              #CHEIAS das 8h00 às 09h30, das 11h00 às 17h30 e das 20h00 às 22h00
            if (
                cls.in_time_range(22, 0, time, 8, 0)
#REMOVIDO       or cls.in_time_range(22, 0, time, 0, 0)
#REMOVIDO       or cls.in_time_range(0, 0, time, 2, 0)
            ):
                return ph.VAZIO_NORMAL                                              #VAZIO das 22h00 às 08h00
#NÃO EXISTE if cls.in_time_range(2, 0, time, 6, 0):
#NÃO EXISTE     return ph.SUPER_VAZIO


MAPPING = {str(Ciclo_Semanal_a()): Ciclo_Semanal_a, str(Ciclo_Diario_a()): Ciclo_Diario_a}    #Adicionado o "_a" para diferenciar do continental e corresponder às CLASS acima(?)
