import mysql.connector

# 데이터베이스 연결 
def connect_db():
    try:
        connection = mysql.connector.connect(
            host="192.168.56.103",
            user="rhyuna",
            password="1234",
            database="SWCLUB",
            port=4567
        )
        print("MySQL 서버 연결 성공!")
        return connection
    except mysql.connector.Error as err:
        print(f"데이터베이스 연결 에러: {err}")
        return None


# 동아리가 데이터베이스에 존재하는지 확인하는 함수
def check_club_exists(cursor, user_club):
    query = "SELECT clubname FROM club WHERE clubname = %s"
    cursor.execute(query, (user_club,))
    result = cursor.fetchone()
    return result is not None

# 회원가입 
def register(connection):
    cursor = connection.cursor()
    try:
        print("\n회원가입을 진행합니다.")
        uid = input("학번을 입력하세요: ")  
        username = input("사용자 이름 입력: ")
        userphonenumber = input("사용자 전화번호 입력: ")
        user_club = input("소속 동아리 입력: ")

        # 동아리가 존재하는지 확인
        if not check_club_exists(cursor, user_club):
            print(f"입력한 동아리 '{user_club}'는 존재하지 않습니다. 다른 동아리를 입력해 주세요.")
            return

        # 회원추가
        insert_query = "INSERT INTO user (Uid, username, userphonenumber, user_club) VALUES (%s, %s, %s, %s)"
        cursor.execute(insert_query, (uid, username, userphonenumber, user_club))
        connection.commit()
        print("회원가입 성공!")
    except mysql.connector.Error as err:
        print(f"회원가입 에러: {err}")
        connection.rollback()

# 로그인 함수
def login(connection):
    cursor = connection.cursor()
    try:
        print("\n로그인을 진행합니다.")
        uid = input("학번을 입력하세요: ")  
        userphonenumber = input("사용자 전화번호 입력: ")

        # 사용자 인증
        auth_query = "SELECT username, user_club FROM user WHERE Uid = %s AND userphonenumber = %s"
        cursor.execute(auth_query, (uid, userphonenumber))
        result = cursor.fetchone()

        if result:
            print(f"로그인 성공! {result[0]}님은 {result[1]} 동아리에 소속되어 있습니다.")
            return result[0], result[1]  #사용자 이름과 동아리 이름
        else:
            print("로그인 실패: 학번 또는 전화번호를 확인하세요.")
            return None, None
    except mysql.connector.Error as err:
        print(f"로그인 에러: {err}")
        return None, None

# 동아리 일정 
def manage_schedule(connection, user_club):
    cursor = connection.cursor()
    while True:
        print(f"\n{user_club} 동아리의 일정을 관리합니다.")
        view_schedules(connection, user_club)
        print("1. 일정 등록")
        print("2. 일정 수정")
        print("3. 일정 삭제")
        print("4. 뒤로 가기")
        choice = input("선택: ")

        if choice == "1":
            register_schedule(connection, user_club)
        elif choice == "2":
            update_schedule(connection, user_club)
        elif choice == "3":
            delete_schedule(connection, user_club)
        elif choice == "4":
            break
        else:
            print("잘못된 선택입니다. 다시 시도하세요.")

# 동아리의 모든 일정을 출력
def view_schedules(connection, user_club):
    cursor = connection.cursor()
    try:
        
        query = "SELECT schedule_id, event_name, event_date, event_time FROM schedule WHERE clubname = %s"
        cursor.execute(query, (user_club,))
        schedules = cursor.fetchall()

        if schedules:
            print(f"{user_club} 동아리의 일정 목록:")
            for schedule in schedules:
                print(f"ID: {schedule[0]} | 이벤트 이름: {schedule[1]} | 날짜: {schedule[2]} | 시간: {schedule[3]}")
        else:
            print(f"{user_club} 동아리에는 등록된 일정이 없습니다.")
    except mysql.connector.Error as err:
        print(f"일정 조회 에러: {err}")

# 동아리 일정 등록
def register_schedule(connection, user_club):
    cursor = connection.cursor()
    try:
        print(f"\n{user_club} 동아리의 일정을 등록합니다.")
        view_schedules(connection, user_club)
        event_name = input("이벤트 이름을 입력하세요: ")
        event_date = input("이벤트 날짜를 입력하세요 (YYYY-MM-DD): ")
        event_time = input("이벤트 시간을 입력하세요 (HH:MM): ")

       #등록
        insert_query = "INSERT INTO schedule (clubname, event_name, event_date, event_time) VALUES (%s, %s, %s, %s)"
        cursor.execute(insert_query, (user_club, event_name, event_date, event_time))
        connection.commit()
        print("일정 등록 성공!")
    except mysql.connector.Error as err:
        print(f"일정 등록 에러: {err}")
        connection.rollback()

# 동아리 일정 수정
def update_schedule(connection, user_club):
    cursor = connection.cursor()
    try:
        print(f"\n{user_club} 동아리의 일정을 수정합니다.")
        view_schedules(connection, user_club)
        event_id = input("수정할 이벤트의 ID를 입력하세요: ")
        event_name = input("새로운 이벤트 이름을 입력하세요: ")
        event_date = input("새로운 이벤트 날짜를 입력하세요 (YYYY-MM-DD): ")
        event_time = input("새로운 이벤트 시간을 입력하세요 (HH:MM): ")

        # 수정
        update_query = "UPDATE schedule SET event_name = %s, event_date = %s, event_time = %s WHERE id = %s AND clubname = %s"
        cursor.execute(update_query, (event_name, event_date, event_time, event_id, user_club))
        connection.commit()
        print("일정 수정 성공!")
    except mysql.connector.Error as err:
        print(f"일정 수정 에러: {err}")
        connection.rollback()

# 동아리 일정 삭제
def delete_schedule(connection, user_club):
    cursor = connection.cursor()
    try:
        print(f"\n{user_club} 동아리의 일정을 삭제합니다.")
        view_schedules(connection, user_club)
        event_id = input("삭제할 이벤트의 ID를 입력하세요: ")

        # 삭제
        delete_query = "DELETE FROM schedule WHERE id = %s AND clubname = %s"
        cursor.execute(delete_query, (event_id, user_club))
        connection.commit()
        print("일정 삭제 성공!")
    except mysql.connector.Error as err:
        print(f"일정 삭제 에러: {err}")
        connection.rollback()


#동아리 회원관리 
def manage_clubmember(connection, user_club):
    cursor = connection.cursor()
    while True:
        print(f"\n{user_club} 동아리의 회원을 관리합니다.")
        
        print("1. 회원 등록 승인")
        print("2. 회원 보기 ")
        
        choice = input("선택: ")

        if choice == "1":#회원 등록 승인해주기
           approve_clubmember(connection, user_club)
        elif choice == "2":#회원모두보기
            view_clubmember(connection, user_club)
            break
        else:
            print("잘못된 선택입니다. 다시 시도하세요.")




def approve_clubmember(connection, user_club):
    cursor = connection.cursor()
    
    try:
        # 대기 중인 회원 조회 
        query = """
        SELECT r.RegisterUid, r.register_id, r.membername, r.memberdepartment, r.memberphonenumber
        FROM register r
        WHERE r.register_clubname = %s AND r.approval_status = 0
        """
        cursor.execute(query, (user_club,))
        pending_members = cursor.fetchall()

        if not pending_members:
            print(f"{user_club} 동아리에는 승인 대기 중인 회원이 없습니다.")
            return

        #대기 중인 회원 목록 
        print(f"{user_club} 동아리의 대기 중인 회원 목록:")
        for member in pending_members:
            print(f"학번: {member[1]}, 이름: {member[2]}, 학과: {member[3]}, 전화번호: {member[4]}")

       
        uid_to_approve = input("승인할 회원의 학번을 입력하세요: ")

        #clubmember 테이블 삽입
        insert_query = """
        INSERT INTO clubmember (memberUid, membername, memberdepartment, memberphonenumber)
        SELECT register_id, membername, memberdepartment, memberphonenumber
        FROM register
        WHERE RegisterUid = %s
        """
        cursor.execute(insert_query, (uid_to_approve,))
        connection.commit()

        # 상태를 '1'로 업데이트
        update_query = """
        UPDATE register
        SET approval_status = 1
        WHERE RegisterUid = %s
        """
        cursor.execute(update_query, (uid_to_approve,))
        connection.commit()

        print(f"{uid_to_approve} 학번의 회원이 승인되었습니다.")

    except mysql.connector.Error as err:
        print(f"에러 발생: {err}")
        connection.rollback()
    finally:
        cursor.close()


# 동아리 회원 모두 보기
def view_clubmember(connection, user_club):
    cursor = connection.cursor()
    try:
        print(f"\n{user_club} 동아리의 모든 회원을 조회합니다.")
        
        # 동아리의 승인된 회원 목록 조회
        query = "SELECT Uid, username, userphonenumber FROM user WHERE user_club = %s AND status = 'approved'"
        cursor.execute(query, (user_club,))
        members = cursor.fetchall()

        if members:
            print(f"{user_club} 동아리의 승인된 회원 목록:")
            for member in members:
                print(f"학번: {member[0]}, 이름: {member[1]}, 전화번호: {member[2]}")
        else:
            print(f"{user_club} 동아리에는 승인된 회원이 없습니다.")
    except mysql.connector.Error as err:
        print(f"회원 조회 에러: {err}")

# 로그인 후 메뉴
def logged_in_menu(connection, username, user_club):
    while True:
        print("\n메뉴:")
        print("1. 동아리 일정 관리")
        print("2. 동아리 회원 관리")
        print("3. 강의실 신청 관리")
        print("4. 로그아웃")
        choice = input("선택: ")

        if choice == "1":
            manage_schedule(connection, user_club)
        elif choice == "2":
            manage_clubmember(connection, user_club)
        # elif choice == "3":
        #     manage_classroom(connection)
        elif choice == "4":
            print(f"{username}님, 로그아웃되었습니다.")
            break
        else:
            print("잘못된 선택입니다. 다시 시도하세요.")


def main():
    connection = connect_db()
    if connection:
        try:
            while True:
                print("\n메뉴:")
                print("1. 회원가입")
                print("2. 로그인")
                print("3. 종료")
                choice = input("선택: ")

                if choice == "1":
                    register(connection)
                elif choice == "2":
                    username, user_club = login(connection)
                    if username and user_club:
                        logged_in_menu(connection, username, user_club)
                elif choice == "3":
                    print("프로그램을 종료합니다.")
                    break
                else:
                    print("잘못된 선택입니다. 다시 시도하세요.")
        finally:
            connection.close()

if __name__ == "__main__":
    main()
