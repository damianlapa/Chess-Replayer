from psycopg2 import connect, OperationalError


def connect_to_database(user, password, database):
    try:
        cnx = connect(user=user, password=password, host='localhost', database=database)
        print('connection succeeded')
        return cnx
    except OperationalError:
        print('connection failed')


def save_game_to_database(game):
    cnx = connect_to_database()
    sql = '''
    INSERT INTO games(game_pgn) VALUES('{}')
    RETURNING game_id
    '''.format(game)
    try:
        cursor = cnx.cursor()
        cursor.execute(sql)
        cnx.commit()
        game_id = cursor.fetchone()[0]
        cursor.close()
    except OperationalError:
        pass
    cnx.close()
    return game_id


def load_game_from_database():
    game_pgn = None
    data = []
    cnx = connect_to_database()
    sql = '''
    SELECT * FROM games
    '''
    try:
        cursor = cnx.cursor()
        cursor.execute(sql)
        cnx.commit()
        for x in cursor:
            data.append(x)

        cursor.close()
    except IndexError:
        print('not_ok')
    cnx.close()
    print(data[2])
    game_pgn = data[2][1]
    if game_pgn:
        return game_pgn


def update_game(game_id, game):
    cnx = connect_to_database()
    sql = f'''
    UPDATE games
    SET game_pgn='{game}'
    WHERE game_id={game_id}
    RETURNING game_id'''
    try:
        cursor = cnx.cursor()
        cursor.execute(sql)
        cnx.commit()
        cursor.close()
    except OperationalError:
        pass
    cnx.close()


def return_all_games():
    all_games = []
    cnx = connect_to_database()
    sql = '''
    SELECT game_pgn from games'''
    try:
        cursor = cnx.cursor()
        cursor.execute(sql)
        cnx.commit()
        for game in cursor:
            all_games.append(game[0])
        cursor.close()
    except OperationalError:
        pass
    cnx.close()
    return all_games
