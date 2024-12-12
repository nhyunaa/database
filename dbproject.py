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
        auth_query = "SELECT Uid, username, user_club FROM user WHERE Uid = %s AND userphonenumber = %s"
        cursor.execute(auth_query, (uid, userphonenumber))
        result = cursor.fetchone()

        if result:
            print(f"로그인 성공! {result[0]} {result[1]}님은 {result[2]} 동아리에 소속되어 있습니다.")
            return result[0], result[1], result[2]  # 학번, 사용자 이름, 동아리 이름
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
        delete_query = "DELETE FROM schedule WHERE schedule_id = %s AND clubname = %s"
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
            view_clubmember(connection,user_club)
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

        # 승인할 회원 선택
        uid_to_approve = input("승인할 회원의 학번을 입력하세요: ")

       
        # 상태를 1로 승인
        update_query = """
        UPDATE register
        SET approval_status = 1
        WHERE register_id = %s
        """
        cursor.execute(update_query, (uid_to_approve,))
        connection.commit()

        print(f"{uid_to_approve} 학번의 회원이 승인되었습니다.")

 # clubmember 테이블에 해당 회원 추가 (register_clubname 포함)
        insert_query = """
        INSERT INTO clubmember (memberUid, membername, memberdepartment, memberphonenumber, register_clubname)
        SELECT register_id, membername, memberdepartment, memberphonenumber, register_clubname
        FROM register
        WHERE register_id = %s
        """
        cursor.execute(insert_query, (uid_to_approve,))
        connection.commit()

        print(f"{uid_to_approve} 학번의 회원이 동아리 회원으로 추가되었습니다.")

    except mysql.connector.Error as err:
        print(f"에러 발생: {err}")
        connection.rollback()
    finally:
        cursor.close()


#동아리 회원 조회
def view_clubmember(connection, user_club):
    cursor = connection.cursor()
    try:
        query = """
                   SELECT * from (
            SELECT c.clubname, cm.membername as names ,cm.memberUid as stn
            FROM 
                club c
            JOIN 
                clubmember cm ON c.clubname  = cm.register_clubname
            UNION
            SELECT c.clubname, u.username as names, u.Uid as stn
            FROM club c JOIN 
                user u ON c.clubname  = u.user_club) AS union_talbe
            WHERE clubname = %s;
        """
        cursor.execute(query, (user_club,))
        members = cursor.fetchall()

        if members:
            print(f"{user_club}동아리 회원 목록")
            for member in members:
                print(f"학번: {member[2]} 이름: {member[1]}")
        else:
            print(f"{user_club} 동아리에는 등록된 회원이 없습니다.")
    except mysql.connector.Error as err:
        print(f"회원 조회 에러: {err}")
    finally:
        cursor.close()

# 강의실 관리
def manage_classroom(connection, user_id, user_club):
    cursor = connection.cursor()
    while True:
        print("1. 강의실 신청")
        print("2. 강의실 예약 상태 확인")
        print("3. 뒤로 가기")
        choice = input("선택: ")

        if choice == "1":
            apply_classroom(connection, user_id, user_club)
        elif choice == "2":
            view_classroom_status(connection, user_id, user_club)
        elif choice == "3":


            break
        else:
            print("잘못된 선택입니다. 다시 시도하세요.")
def view_classroom(connection):
    cursor = connection.cursor()
    try:
        # 강의실 목록 조회 쿼리
        query = "SELECT classroom_id, classroom_name, occupancy FROM classroom"
        cursor.execute(query)
        classrooms = cursor.fetchall()

        if classrooms:
            print(f"강의실 목록:")
            for classroom in classrooms:
                print(f"ID: {classroom[0]} | 강의실 이름: {classroom[1]} | 수용 인원: {classroom[2]}")
        else:
            print(f"남은 강의실이 존재하지 않습니다.")
    except mysql.connector.Error as err:
        print(f"강의실 조회 에러: {err}")

def apply_classroom(connection, user_id, user_club):
    cursor = connection.cursor()
    view_classroom(connection)
    try:
        # 강의실 ID와 예약 시간 입력 받기
        classroom_id = input("예약할 강의실 ID를 입력하세요: ").strip()
        rent_start = input("예약 시작 시간 (YYYY-MM-DD HH:MM)을 입력하세요: ").strip()
        rent_end = input("예약 종료 시간 (YYYY-MM-DD HH:MM)을 입력하세요: ").strip()
        print('강의실 번호 ',classroom_id)
        print('-----Error------ 사용자 아이디: ', user_id)

        print('시작시간', rent_start)
        print('종료시간', rent_end)

        # 입력값 검증
        if not classroom_id or not rent_start or not rent_end:
            print("모든 입력값을 정확히 입력해주세요.")
            return

        # 겹치는 예약 확인 쿼리
        overlap_query = """
            SELECT COUNT(*) FROM rent
            WHERE apply_classroomid = %s
            AND (
                (rent_start < %s AND rent_end > %s) 
                OR (rent_start < %s AND rent_end > %s)
                OR (rent_start >= %s AND rent_end <= %s)
            );
        """

        cursor.execute(overlap_query, (classroom_id, rent_end, rent_end, rent_start, rent_start, rent_start, rent_end))
        overlap_count = cursor.fetchone()[0]

        if overlap_count > 0:
           print("예약 시간이 겹칩니다. 다른 시간을 선택해주세요.")
           return
        print('line ----------------------')
        
        # 예약 입력 쿼리
        insert_query = """
            INSERT INTO rent (apply_classroomid, user_id, rent_start, rent_end)
            VALUES (%s, %s, %s, %s);
        """

        # 올바르게 바인딩된 값 전달
        cursor.execute(insert_query, (classroom_id, user_id, rent_start, rent_end))
        connection.commit()

        print(f"강의실 예약 성공! 예약 ID는 {cursor.lastrowid}입니다.")

    except mysql.connector.Error as err:
        print(f"예약 중 에러 발생: {err}")
        connection.rollback()

    finally:
        cursor.close()


# 로그인 후 메뉴
def logged_in_menu(connection, user_id, username, user_club):
    while True:
        print("\n메뉴:")
        print("1. 동아리 일정 관리")
        print("2. 동아리 회원 관리")
        print("3. 강의실 신청")
        print("4. 로그아웃")
        choice = input("선택: ")

        if choice == "1":
            manage_schedule(connection, user_club)
        elif choice == "2":
            manage_clubmember(connection, user_club)
        elif choice == "3":
            manage_classroom(connection, user_id, user_club)
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
                    user_id, username, user_club = login(connection)
                    if user_id and username and user_club:
                        logged_in_menu(connection, user_id, username, user_club)
                elif choice == "3":
                    print("프로그램을 종료합니다.")
                    break
                else:
                    print("잘못된 선택입니다. 다시 시도하세요.")
        finally:
            connection.close()

if __name__ == "__main__":
    main()
