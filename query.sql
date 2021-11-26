CREATE OR REPLACE FUNCTION CadastroUsuario (pass VARCHAR, primeiro_nome_par VARCHAR,sobrenome_par VARCHAR,login_par VARCHAR,
        dominio_par VARCHAR, data_nasc_par DATE, logradouro_par VARCHAR, num_par INTEGER, CEP_par VARCHAR,
        DDD1_par INTEGER ,prefixo1_par INTEGER,num1_par INTEGER,DDD2_par INTEGER,prefixo2_par INTEGER,num2_par INTEGER) returns INTEGER
LANGUAGE plpgsql
AS $$
DECLARE
id_user INTEGER;
BEGIN
--comandos
    INSERT INTO usuario ("password", email, date_joined, primeiro_nome, sobrenome, login, dominio, data_nasc,num, logradouro, CEP, DDD1, prefixo1, num1, DDD2, prefixo2, num2, is_active, is_superuser, is_staff)
                         VALUES (pass, 'lab_bd@gmail.com', localtimestamp, primeiro_nome_par, sobrenome_par, login_par, dominio_par, data_nasc_par,num_par, logradouro_par, CEP_par, DDD1_par, prefixo1_par, num1_par, DDD2_par, prefixo2_par, num2_par, 'true', 'false', 'false')
                         RETURNING id_usuario into id_user;
                         
    RETURN id_user;
COMMIT;
END;$$;


CREATE OR REPLACE PROCEDURE InserePassageiro (cpf_par varchar(11), id_usuario_par int)
LANGUAGE plpgsql
AS $$
BEGIN
--comandos
    INSERT INTO passageiro VALUES (cpf_par, id_usuario_par);
COMMIT;
END;$$;


CREATE OR REPLACE PROCEDURE InsereMotorista (numero_cnh_par int, data_validade_cnh_par date, id_usuario_par int)
LANGUAGE plpgsql
AS $$
BEGIN
--comandos
    INSERT INTO motorista VALUES (numero_cnh_par, data_validade_cnh_par, id_usuario_par);
COMMIT;
END;$$;


CREATE OR REPLACE PROCEDURE CadastroPassageiro (pass varchar, cpf_par varchar(11), primeiro_nome_par VARCHAR,sobrenome_par VARCHAR,login_par VARCHAR,
        dominio_par VARCHAR, data_nasc_par DATE, logradouro_par VARCHAR, num_par INTEGER, CEP_par VARCHAR,
        DDD1_par INTEGER ,prefixo1_par INTEGER,num1_par INTEGER,DDD2_par INTEGER,prefixo2_par INTEGER,num2_par INTEGER)
LANGUAGE plpgsql
AS $$
DECLARE
id_user INTEGER;
BEGIN
--comandos
    id_user = CadastroUsuario(pass, primeiro_nome_par, sobrenome_par, login_par, dominio_par, data_nasc_par, 
                                                            logradouro_par, num_par, CEP_par, DDD1_par, prefixo1_par, num1_par, DDD2_par,
                                                            prefixo2_par, num2_par);
    call InserePassageiro(cpf_par, id_user);
COMMIT;
END;$$;


CREATE OR REPLACE PROCEDURE CadastroMotorista (pass varchar, numero_cnh_par int, data_validade_cnh_par date, primeiro_nome_par VARCHAR,
        sobrenome_par VARCHAR,login_par VARCHAR, dominio_par VARCHAR, data_nasc_par DATE, logradouro_par VARCHAR, num_par INTEGER,
        CEP_par VARCHAR,DDD1_par INTEGER ,prefixo1_par INTEGER,num1_par INTEGER,DDD2_par INTEGER,prefixo2_par INTEGER,num2_par INTEGER)
LANGUAGE plpgsql
AS $$
DECLARE
id_user INTEGER;
BEGIN
--comandos
    id_user = CadastroUsuario(pass, primeiro_nome_par, sobrenome_par, login_par, dominio_par, data_nasc_par, 
                                                            logradouro_par, num_par, CEP_par, DDD1_par, prefixo1_par, num1_par, DDD2_par,
                                                            prefixo2_par, num2_par);
    call InsereMotorista(numero_cnh_par, data_validade_cnh_par, id_user);
COMMIT;
END;$$;


CREATE OR REPLACE PROCEDURE CadastroPassageiroMotorista (pass varchar, cpf_par varchar(11),numero_cnh_par int, data_validade_cnh_par date, primeiro_nome_par VARCHAR,
        sobrenome_par VARCHAR,login_par VARCHAR, dominio_par VARCHAR, data_nasc_par DATE, logradouro_par VARCHAR, num_par INTEGER,
        CEP_par VARCHAR,DDD1_par INTEGER ,prefixo1_par INTEGER,num1_par INTEGER,DDD2_par INTEGER,prefixo2_par INTEGER,num2_par INTEGER)
LANGUAGE plpgsql
AS $$
DECLARE
id_user INTEGER;
BEGIN
--comandos
    id_user = CadastroUsuario(pass, primeiro_nome_par, sobrenome_par, login_par, dominio_par, data_nasc_par, 
                                                            logradouro_par, num_par, CEP_par, DDD1_par, prefixo1_par, num1_par, DDD2_par,
                                                            prefixo2_par, num2_par);
    call InserePassageiro(cpf_par, id_user);
    call InsereMotorista(numero_cnh_par, data_validade_cnh_par, id_user);
COMMIT;
END;$$;

CREATE OR REPLACE FUNCTION lista_motoristas (refcursor) RETURNS REFCURSOR
LANGUAGE plpgsql
AS $$
BEGIN
    OPEN $1 FOR SELECT mo.numero_cnh, mo.id_usuario, us.primeiro_nome, us.sobrenome 
        FROM motorista AS mo
        INNER JOIN usuario AS us ON mo.id_usuario = us.id_usuario;
    RETURN $1;

    COMMIT;
END; $$;

CREATE PROCEDURE insere_ponto (_latitude in int, _longitude in int, 
                               _cep in varchar, _num in int,
                               _logradouro in varchar, _nome in varchar, 
                               _ponto_referencia in varchar DEFAULT NULL::varchar)
LANGUAGE plpgsql
AS $$
BEGIN
    insert into PONTO (latitude,longitude,cep,num,logradouro,ponto_referencia,nome) 
    values(_latitude,_longitude,_cep,_num,_logradouro, _ponto_referencia,_nome);
    COMMIT;
END; $$;


CREATE OR REPLACE PROCEDURE CadastroPossui
-- params
    (id_user INTEGER, placa_p CHARACTER VARYING, modelo CHARACTER VARYING, n_assentos INTEGER, cor CHARACTER VARYING, ano INTEGER)
LANGUAGE plpgsql
AS $$
BEGIN
-- comandos
    IF NOT EXISTS (SELECT v.placa FROM veiculo v WHERE v.placa = placa_p)
    THEN
        CALL Cadastroveiculo(placa_p, modelo, n_assentos, cor, ano);
    END IF;
    INSERT INTO POSSUI (id_motorista, placa) VALUES (id_user, placa_p);
COMMIT;
END; $$;

CREATE OR REPLACE PROCEDURE CadastroVeiculo
-- params
    (placa CHARACTER VARYING, modelo CHARACTER VARYING, n_assentos INTEGER, cor CHARACTER VARYING, ano INTEGER)
LANGUAGE SQL
AS $$
-- comandos
    INSERT INTO VEICULO values (placa, modelo, n_assentos, cor, ano);
$$;

CREATE OR REPLACE FUNCTION lista_veiculos_disponiveis (refcursor, cod_motorista in int) RETURNS REFCURSOR
LANGUAGE plpgsql
AS $$
BEGIN
    OPEN $1 FOR SELECT p.id_possui, p.placa, v.modelo, v.n_assentos, v.cor, v.ano 
        FROM possui p
        INNER JOIN veiculo v ON (p.placa = v.placa)
        WHERE id_motorista = cod_motorista;

    RETURN $1;

    COMMIT;
END; $$;

CREATE OR REPLACE FUNCTION pontos(REFCURSOR) RETURNS REFCURSOR
LANGUAGE plpgsql
AS
$$
BEGIN
    OPEN $1 FOR SELECT id_ponto, nome, logradouro, num, cep FROM ponto;
    RETURN $1;
END; $$;

CREATE OR REPLACE PROCEDURE cadastro_oferta_carona(ID_Possui_Ofertante in INT, data_partida_oferta in DATE, 
                                                   hora_partida_oferta in TIME, n_vagas_oferta in INT, 
                                                   ponto_final_p in INT, ponto_inicial_p in INT)
LANGUAGE plpgsql AS $$
DECLARE
id_oferta_carona INTEGER;
BEGIN
--comandos
    id_oferta_carona = insere_oferta_carona(ID_Possui_Ofertante, data_partida_oferta, 
                                                hora_partida_oferta, n_vagas_oferta);
    call insere_passa_por(id_oferta_carona, ponto_inicial_p,
                                  'false', 'true');
    call insere_passa_por(id_oferta_carona, ponto_final_p,
                                    'true', 'false');
COMMIT;
END;$$;

CREATE OR REPLACE FUNCTION insere_oferta_carona(ID_Possui_Ofertante in INT, data_partida_oferta in DATE, 
                                                hora_partida_oferta in TIME, n_vagas_oferta in INT) returns INTEGER
    LANGUAGE plpgsql AS $$
    DECLARE
    id_oferta_carona INTEGER;
    BEGIN
        INSERT INTO OFERTA_DE_CARONA (ID_Possui,data_partida,horario_partida,vagas_ofertadas, vagas_disponiveis)
                              VALUES (ID_Possui_Ofertante, data_partida_oferta, hora_partida_oferta, 
                                      n_vagas_oferta, n_vagas_oferta) RETURNING id_oferta_de_carona into id_oferta_carona;
        RETURN id_oferta_carona;
        COMMIT;
    END; $$;

CREATE OR REPLACE PROCEDURE insere_passa_por(ID_oferta_de_carona_p in INTEGER,id_ponto_p in INTEGER,
                                  ponto_final_p in BOOLEAN, ponto_inicial_p in BOOLEAN)
    LANGUAGE plpgsql AS $$ 
        BEGIN
            INSERT INTO PASSA_POR (ID_oferta_de_carona,id_ponto, ponto_final, ponto_inicial)
                                  VALUES (ID_oferta_de_carona_p,id_ponto_p, ponto_final_p, ponto_inicial_p);
            COMMIT;
        END; $$;

CREATE OR REPLACE VIEW pontos_registrados AS SELECT
  * FROM ponto;

CREATE OR REPLACE VIEW lista_caronas_oferecidas AS
SELECT o.data_partida, 
    o.horario_partida,
    o.vagas_ofertadas,
    o.vagas_disponiveis,
    v.modelo, 
    v.placa,
    moto.id_usuario
    FROM oferta_de_carona o 
    INNER JOIN possui p ON (o.id_possui = p.id_possui)
    INNER JOIN veiculo v ON (p.placa = v.placa)
    INNER JOIN motorista moto ON (p.id_motorista = moto.id_usuario)
    
CREATE OR REPLACE FUNCTION insere_agendamento (_cpf in varchar(11), _horario_agendamento in timestamp, 
                               _id_ponto_origem in int, _id_ponto_destino in int,
                               _data_partida in date, _horario_partida in time, 
                               _atraso_aceitavel in int, _adiantamento_aceitavel in int,
                               _ativo in int default 1) RETURNS INTEGER
LANGUAGE plpgsql
AS $$
DECLARE
id_agend INTEGER;
BEGIN
    insert into agendamento (cpf, horario_agendamento, id_ponto_origem, id_ponto_destino, 
                             data_partida, horario_partida, atraso_aceitavel, adiantam_aceitavel, ativo) 
    values(_cpf,_horario_agendamento, _id_ponto_origem, _id_ponto_destino, _data_partida, 
           _horario_partida, _atraso_aceitavel, _adiantamento_aceitavel, _ativo) returning id_agendamento into id_agend;
    RETURN id_agend;
    COMMIT;
END; $$

CREATE OR REPLACE FUNCTION gera_match() RETURNS trigger
LANGUAGE plpgsql
AS $$
DECLARE
datahora timestamp;
matchview record;
BEGIN
    datahora = new.data_partida + new.horario_partida;
    for matchview in select ID_Oferta_de_carona from oferta_de_carona oc
    WHERE (data_partida + horario_partida) >= (datahora - new.adiantam_aceitavel * interval '1 minute')
    AND (data_partida + horario_partida) <= (datahora + new.atraso_aceitavel * interval '1 minute')
    AND (new.id_ponto_origem in (select id_ponto from passa_por p where p.id_oferta_de_carona = oc.id_oferta_de_carona))
    AND (new.id_ponto_destino in (select id_ponto from passa_por p where p.id_oferta_de_carona = oc.id_oferta_de_carona)) LOOP
        insert into _match (id_agendamento, id_oferta_de_carona) values (new.id_agendamento, matchview.id_oferta_de_carona);
   END LOOP;

    RETURN NEW;
    COMMIT;
END; $$


CREATE TRIGGER trigger_gera_match AFTER INSERT ON agendamento
    FOR EACH ROW EXECUTE PROCEDURE gera_match();


CREATE VIEW lista_matches AS
SELECT m.id_agendamento, o.data_partida, o.horario_partida, o.vagas_disponiveis, po_origem.nome as ponto_origem, po_destino.nome as ponto_destino,
    u.primeiro_nome, mot.nota_media, mot.data_validade_cnh, v.modelo, v.n_assentos
    FROM _match m 
    INNER JOIN agendamento a ON (m.id_agendamento = a.id_agendamento)
    INNER JOIN oferta_de_carona o ON (o.id_oferta_de_carona = m.id_oferta_de_carona)
    INNER JOIN passa_por p_destino ON (p_destino.id_oferta_de_carona = o.id_oferta_de_carona AND p_destino.ponto_final = true)
    INNER JOIN passa_por p_origem ON (p_origem.id_oferta_de_carona = o.id_oferta_de_carona AND p_origem.ponto_inicial = true)
    INNER JOIN ponto po_origem ON (p_origem.id_ponto = po_origem.id_ponto)
    INNER JOIN ponto po_destino ON (p_destino.id_ponto = po_destino.id_ponto)
    INNER JOIN possui p ON (p.id_possui = o.id_possui)
    INNER JOIN motorista mot ON (mot.id_usuario = p.id_motorista)
    INNER JOIN usuario u ON (u.id_usuario = mot.id_usuario)
    INNER JOIN veiculo v ON (v.placa = p.placa)
    