from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin


class Usuario(AbstractUser, PermissionsMixin):
    id_usuario = models.AutoField(primary_key=True)
    primeiro_nome = models.CharField(max_length=50)
    sobrenome = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True, db_column='login')
    dominio = models.CharField(max_length=50)
    data_nasc = models.DateField()
    num = models.IntegerField()
    logradouro = models.CharField(max_length=50)
    cep = models.CharField(max_length=9)
    ddd1 = models.IntegerField()
    prefixo1 = models.IntegerField()
    num1 = models.IntegerField()
    ddd2 = models.IntegerField(blank=True, null=True)
    prefixo2 = models.IntegerField(blank=True, null=True)
    num2 = models.IntegerField(blank=True, null=True)
    is_active = is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    first_name = None
    last_name = None

    EMAIL_FIELD = 'dominio'
    REQUIRED_FIELDS = [
        'primeiro_nome', 'sobrenome', 'data_nasc', 'num', 'logradouro',
        'cep', 'ddd1', 'prefixo1', 'num1',
    ]

    class Meta:
        managed = True
        db_table = 'usuario'

    def get_full_name(self):
        """Retrieve full name of user"""
        return f"{self.primeiro_nome} {self.sobrenome}"

    def get_short_name(self):
        """Retrive short name"""
        return self.primeiro_nome


class Agendamento(models.Model):
    id_agendamento = models.AutoField(primary_key=True)
    cpf = models.ForeignKey('Passageiro', models.DO_NOTHING, db_column='cpf')
    horario_agendamento = models.DateTimeField()
    id_ponto_origem = models.ForeignKey('Ponto', models.DO_NOTHING, related_name='origem', db_column='id_ponto_origem')
    id_ponto_destino = models.ForeignKey('Ponto', models.DO_NOTHING, related_name='destino', db_column='id_ponto_destino')
    data_partida = models.DateField()
    horario_partida = models.TimeField()
    atraso_aceitavel = models.IntegerField()
    adiantam_aceitavel = models.IntegerField()
    ativo = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'agendamento'
        unique_together = (('cpf', 'horario_agendamento'),)


class Carona(models.Model):
    id_reserva = models.OneToOneField('Reserva', models.DO_NOTHING, db_column='id_reserva', primary_key=True)
    horario_saida = models.TimeField()
    horario_chegada = models.TimeField()
    avaliacao_motorista = models.TextField(blank=True, null=True)
    avaliacao_passageiro = models.TextField(blank=True, null=True)
    nota_passageiro = models.IntegerField(blank=True, null=True)
    nota_motorista = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'carona'
        unique_together = (('id_reserva', 'horario_saida', 'horario_chegada'),)


class Motorista(models.Model):
    numero_cnh = models.IntegerField()
    data_validade_cnh = models.DateField()
    id_usuario = models.OneToOneField('Usuario', models.DO_NOTHING, db_column='id_usuario', primary_key=True)
    nota_media = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'motorista'
        unique_together = (('numero_cnh', 'data_validade_cnh'),)


class OfertaDeCarona(models.Model):
    id_oferta_de_carona = models.AutoField(primary_key=True)
    id_possui = models.ForeignKey('Possui', models.DO_NOTHING, db_column='id_possui')
    data_partida = models.DateField()
    horario_partida = models.TimeField()
    vagas_ofertadas = models.IntegerField()
    vagas_disponiveis = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'oferta_de_carona'
        unique_together = (('id_possui', 'data_partida', 'horario_partida'),)


class PassaPor(models.Model):
    id_oferta_de_carona = models.OneToOneField(OfertaDeCarona, models.DO_NOTHING, db_column='id_oferta_de_carona', primary_key=True)
    id_ponto = models.ForeignKey('Ponto', models.DO_NOTHING, db_column='id_ponto')
    ponto_final = models.BooleanField()
    ponto_inicial = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'passa_por'
        unique_together = (('id_oferta_de_carona', 'id_ponto'),)


class Passageiro(models.Model):
    cpf = models.CharField(primary_key=True, max_length=11)
    id_usuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='id_usuario')
    nota_media = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'passageiro'


class Ponto(models.Model):
    id_ponto = models.AutoField(primary_key=True)
    latitude = models.IntegerField()
    longitude = models.IntegerField()
    cep = models.CharField(max_length=9)
    num = models.IntegerField()
    logradouro = models.CharField(max_length=50)
    ponto_referencia = models.CharField(max_length=100, blank=True, null=True)
    nome = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'ponto'
        unique_together = (('latitude', 'longitude'),)


class Possui(models.Model):
    id_possui = models.AutoField(primary_key=True)
    id_motorista = models.ForeignKey(Motorista, models.DO_NOTHING, db_column='id_motorista')
    placa = models.ForeignKey('Veiculo', models.DO_NOTHING, db_column='placa')

    class Meta:
        managed = False
        db_table = 'possui'
        unique_together = (('id_motorista', 'placa'),)


class Match(models.Model):
    id_match = models.AutoField(primary_key=True)
    id_agendamento = models.ForeignKey('Agendamento', models.DO_NOTHING, db_column='id_agendamento')
    id_oferta_de_carona = models.ForeignKey('OfertaDeCarona', models.DO_NOTHING, db_column='id_oferta_de_carona')

    class Meta:
        managed = False
        db_table = '_match'
        unique_together = (('id_agendamento', 'id_oferta_de_carona'),)


class Reserva(models.Model):
    id_reserva = models.AutoField(primary_key=True)
    id_match = models.OneToOneField(Match, models.DO_NOTHING, db_column='id_match')

    class Meta:
        managed = False
        db_table = 'reserva'


class Veiculo(models.Model):
    placa = models.CharField(primary_key=True, max_length=7)
    modelo = models.CharField(max_length=255)
    n_assentos = models.IntegerField()
    cor = models.CharField(max_length=50)
    ano = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'veiculo'
